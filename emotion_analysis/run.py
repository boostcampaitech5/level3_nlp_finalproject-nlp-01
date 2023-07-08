# koBERT
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

# Transformers
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

from sklearn.model_selection import train_test_split

# Setting Library
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook
import pandas as pd
import argparse
from datetime import datetime
from pytz import timezone

from model import BERTDataset, BERTClassifier, calc_accuracy
from utils import get_data, preprocessing_data, write_log, predict_model

def main(args):
    '''
        ###################################    모델 학습 시작    ###################################
    '''
    device = torch.device("cuda:0")     # device 설정
    
    # BERT 모델, Vocabulary 불러오기
    bertmodel, vocab = get_pytorch_kobert_model(cachedir=".cache")
    
    ## 1. 데이터셋 전처리
    data_path = f"./data/{args.file}"
    data_list = preprocessing_data(data_path)

    tokenizer = get_tokenizer()
    dataset_train, dataset_test = train_test_split(data_list, test_size = 0.2, shuffle = True, random_state = 42)
    tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower = False)     # sentencepiece 라이브러리를 사용하는 Tokenizer

    ## 2. 파라미터 값 불러오기
    max_len = int(args.max_len)
    batch_size = int(args.batch)
    warmup_ratio = 0.1
    num_epochs = int(args.epochs)
    max_grad_norm = 1
    log_interval = 200
    learning_rate = float(args.lr)
    dr_rate = float(args.drop_out)

    # BERTDataset : 각 데이터가 BERT 모델의 입력으로 들어갈 수 있도록 tokenization, int encoding, padding하는 함수
    data_train = BERTDataset(dataset_train, 0, 1, tok, vocab, max_len, True, False)
    data_test = BERTDataset(dataset_test, 0, 1, tok, vocab, max_len, True, False)

    # torch 형식의 dataset을 만들어 입력 데이터셋의 전처리 마무리
    train_dataloader = torch.utils.data.DataLoader(data_train, batch_size = batch_size, num_workers = 4)
    test_dataloader = torch.utils.data.DataLoader(data_test, batch_size = batch_size, num_workers = 4)
    
    # BERT  모델 불러오기
    model = BERTClassifier(bertmodel,  dr_rate = dr_rate).to(device)
    
    # optimizer와 schedule 설정
    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    
    optimizer = AdamW(optimizer_grouped_parameters, lr = learning_rate)
    loss_fn = nn.CrossEntropyLoss() # 다중분류를 위한 loss function
    
    t_total = len(train_dataloader) * num_epochs
    warmup_step = int(len(train_dataloader) * warmup_ratio)     # 정확도가 조금 오름
    # warmup_step = int(t_total * warmup_ratio)
    
    scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps = warmup_step, num_training_steps = t_total)

    train_history = []
    test_history = []
    loss_history = []
    log_history = {"train_acc":[], "test_acc":[]}
    
    for e in range(num_epochs):
        train_acc = 0.0
        test_acc = 0.0
        
        '''
                ####################################################################################################
                                                            T r a i n                
                ####################################################################################################
        '''
        model.train()
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(train_dataloader, total = len(train_dataloader))):
            optimizer.zero_grad()
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)
            valid_length= valid_length
            label = label.long().to(device)
            out = model(token_ids, valid_length, segment_ids)
             
            loss = loss_fn(out, label)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()
            scheduler.step()  # Update learning rate schedule
            train_acc += calc_accuracy(out, label)
            if batch_id % log_interval == 0:
                print("epoch {} batch id {} loss {} train acc {}".format(e+1, batch_id+1, loss.data.cpu().numpy(), train_acc / (batch_id+1)))
                train_history.append(train_acc / (batch_id+1))
                loss_history.append(loss.data.cpu().numpy())
        ###
        log_history["train_acc"].append(str(train_acc / (batch_id+1))[:6])
        
        print("epoch {} train acc {}".format(e+1, train_acc / (batch_id+1)))
        train_history.append(train_acc / (batch_id+1))
    
        
        '''
                ####################################################################################################
                                                            e v a l                
                ####################################################################################################
        '''
        # .eval() : nn.Module에서 train time과 eval time에서 수행하는 다른 작업을 수행할 수 있도록 switching 하는 함수
        # 즉, model이 Dropout이나 BatNorm2d를 사용하는 경우, train 시에는 사용하지만 evaluation을 할 때에는 사용하지 않도록 설정해주는 함수
        model.eval()
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(test_dataloader, total = len(test_dataloader))):
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)
            valid_length = valid_length
            label = label.long().to(device)
            out = model(token_ids, valid_length, segment_ids)
            test_acc += calc_accuracy(out, label)
        ###
        log_history["test_acc"].append(str(test_acc / (batch_id+1))[:6])
        print("epoch {} test acc {}".format(e+1, test_acc / (batch_id+1)))
        test_history.append(test_acc / (batch_id+1))

    write_log(args, log_history)
        
    '''
            ####################################################################################################
                                                    p r e d i c t                
            ####################################################################################################
    '''
    predict_model(model, tok, vocab, args, device)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="sentiment_train_data.csv")
    parser.add_argument("-b", "--batch", type=int, default=32)
    parser.add_argument("-e", "--epochs", type=int, default=5)
    parser.add_argument("-ml", "--max_len", type=int, default=256)
    parser.add_argument("-l", "--lr", type=float, default=5e-5)
    parser.add_argument("-do", "--drop_out", type=float, default=0.5)
    args = parser.parse_args()

    main(args)