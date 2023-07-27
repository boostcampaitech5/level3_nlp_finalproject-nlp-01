import json

from constraints import PATH, TAG


# api key와 url 정보 불러오기
def get_textunes_secret():
    with open(PATH.SECRET_FILE, 'r') as file:
        data = json.load(file)

    return data


# music 데이터로 부터 카테고리 정보 불러오기
def get_music_category():
    output = {}
    with open(PATH.DATA_PATH, 'r', encoding='utf-8') as f:
        datas = json.load(f)

    output[TAG.GENRES] = \
        [f"{key} ({value})  *" for key, value in datas[TAG.GENRES][TAG.POPULAR].items()] +\
        [f"{key} ({value})" for key, value in datas[TAG.GENRES]
         [TAG.NORMAL].items()]

    output[TAG.INSTRUMENTS] = \
        [f"{key} ({value})  *" for key, value in (datas[TAG.INSTRUMENTS][TAG.POPULAR]).items()] +\
        [f"{key} ({value})" for key, value in datas[TAG.INSTRUMENTS]
         [TAG.NORMAL].items()]

    output[TAG.MOODS] = \
        [f"{key} ({value})  *" for key, value in datas[TAG.MOODS][TAG.POPULAR].items()] +\
        [f"{key} ({value})" for key, value in datas[TAG.MOODS]
         [TAG.NORMAL].items()]

    output[TAG.ETC] = output[TAG.GENRES] + \
        output[TAG.INSTRUMENTS]+output[TAG.MOODS]
    output[TAG.TEMPO] = ['Auto', 'Slow', 'Medium', 'Fast']
    output[TAG.DURATION] = ['0:15', '0:30', '1:00']

    return output


def get_simple_category():
    output = {}
    with open(PATH.DATA_PATH, 'r', encoding='utf-8') as f:
        datas = json.load(f)

    output[TAG.GENRES] = \
        [f"{key} ({value})" for key, value in datas[TAG.GENRES]
         [TAG.POPULAR].items()]

    output[TAG.INSTRUMENTS] = \
        [f"{key} ({value})" for key, value in datas[TAG.INSTRUMENTS]
         [TAG.POPULAR].items()]

    output[TAG.MOODS] = \
        [f"{key} ({value})" for key, value in datas[TAG.MOODS]
         [TAG.POPULAR].items()]

    output[TAG.ETC] = output[TAG.GENRES] + \
        output[TAG.INSTRUMENTS]+output[TAG.MOODS]
    output[TAG.TEMPO] = ['Auto', 'Slow', 'Medium', 'Fast']
    output[TAG.DURATION] = ['0:15', '0:30', '1:00']

    return output

def get_base_category():
    with open(PATH.DATA_PATH, 'r', encoding='utf-8') as f:
        datas = json.load(f)
    
    return {
        TAG.GENRES: dict(datas[TAG.GENRES][TAG.POPULAR], **datas[TAG.GENRES][TAG.NORMAL]),
        TAG.INSTRUMENTS: dict(datas[TAG.INSTRUMENTS][TAG.POPULAR], **datas[TAG.INSTRUMENTS][TAG.NORMAL]),
        TAG.MOODS: dict(datas[TAG.MOODS][TAG.POPULAR], **datas[TAG.MOODS][TAG.NORMAL]),
    }
