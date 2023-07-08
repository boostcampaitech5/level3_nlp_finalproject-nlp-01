import pandas as pd
import numpy as np
import os

from typing import List
import torch
from model import BERTDataset, BERTClassifier
from tqdm import tqdm

def get_data(data_path:str) -> pd.DataFrame:
    try:    # Unicode를 읽지 못하는 경우가 있어서 try-except 코드 작성
        data = pd.read_csv(data_path, encoding = 'utf-8')
    except UnicodeDecodeError:
        data = pd.read_csv(data_path, encoding = 'cp949')
    
    return data

def preprocessing_data(file_path:str) -> List:
    data = get_data(file_path)
    
    data.loc[(data['target'] == "fear"), 'target'] = 0  #공포 => 0
    data.loc[(data['target'] == "surprise"), 'target'] = 1  #놀람 => 1
    data.loc[(data['target'] == "angry"), 'target'] = 2  #분노 => 2
    data.loc[(data['target'] == "sadness"), 'target'] = 3  #슬픔 => 3
    data.loc[(data['target'] == "neutral"), 'target'] = 4  #중립 => 4
    data.loc[(data['target'] == "happiness"), 'target'] = 5  #행복 => 5
    data.loc[(data['target'] == "disgust"), 'target'] = 6  #혐오 => 6

    data_list = []
    for text, label in zip(data['text'], data['target']):
        data = []   
        data.append(text)
        data.append(str(label))
    
        data_list.append(data)
        
    return data_list

def write_log(args, log_history:List) -> None:
    os.makedirs('./result', exist_ok = True)
    with open(f'./result/{args.file[:-4]}-log.txt', 'a', encoding = 'utf-8') as file:
        train_acc = ' '.join(log_history["train_acc"])
        test_acc = ' '.join(log_history["test_acc"])
        file.write(f"data : {args.file} \t epochs : {args.epochs} \t batch : {args.batch} \t max_len : {args.max_len} \t lr : {args.lr}\n")
        file.write(f"train_acc : {train_acc}\n")
        file.write(f"test_acc : {test_acc}\n")
        file.write("="*50+'\n\n')
        
def predict_model(model, tok, vocab, args, device): # input = 감정분류하고자 하는 sentence
    texts = [
        "아빠는 아들이 레고를 들고 가는 뒷모습을 보고 매우 안쓰러웠어요",
        "많이 힘드시겠어요. 주위에 의논할 상대가 있나요?",
        "부모님의 노여움에 섭섭하시군요. 이런 상황을 어떻게 해결하면 좋을까요?",
        "어제도 야근 오늘도 야근이야. 너무 힘들어.",
        "직장 상사로부터 칭찬을 받았는데 너무 신이 나!",
        "취업 준비 중인데 잘 안 되어 우울해.",
        "여자 친구가 다른 남자랑 연락하는 걸 알게 됐어.",
        "나는 우리 아이들이 무슨 일을 하든 믿고 응원해줄 예정이야.",
        "아내가 오랜만에 만난 친구조차 못 만나게 해.",
        "개인적으로 연금보험을 들어갔는데 내가 모르고 해약을 해버렸어.",
        "오늘 성적이 너무 하락했어. 충격이야.",
        "나 기분이 우울해서 화분을 샀어",
        "왜 넌 항상 니생각만 해?",
        "아니, 너 T야?",
        "친구들이 내 별명을 대놓고 불러서 창피해.",
        "심심한 위로의 말씀을 드리겠습니다.",
        "아니, 심심한 위로는 무슨 장난같은 말이니?",
        "최근 갑자기 폭력을 당하고 있어서 너무 괴로운 마음이야.",
        "어머니가 화를 내시면서 상처 되는 말을 해.",
        "벌이는 적은데 애들도 키워야 하고 부모님도 모셔야 하니 너무 버거워.",
            ]    # 20개
    
    num2pred = {
        0:"공포",  1:"놀람",  2:"분노",  3:"슬픔",  4:"중립",  5:"행복",  6:"혐오"
    }
    
    save_file = []
    for text in tqdm(texts, total=len(texts)):
        
        data = [text, '0']
        dataset_another = [data]

        another_test = BERTDataset(dataset_another, 0, 1, tok, vocab, args.max_len, True, False) # 토큰화한 문장
        test_dataloader = torch.utils.data.DataLoader(another_test, batch_size = args.batch, num_workers = 1) # torch 형식 변환
        
        model.eval() 

        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)

            valid_length = valid_length
            label = label.long().to(device)
            out = model(token_ids, valid_length, segment_ids)

            for i in out: # out = model(token_ids, valid_length, segment_ids)
                logits = i
                logits = logits.detach().cpu().numpy()
                output = num2pred[np.argmax(logits)]
                
        save_file.append(f"{text} => {output}")
    
    with open(f'./result/{args.file[:-4]}-{args.batch}-{args.epochs}-{args.max_len}-{args.lr}-output.txt', 'w', encoding = 'utf-8') as file:
        file.write('\n'.join(save_file))