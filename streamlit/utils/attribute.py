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
        [f"{tag}  *" for tag in datas[TAG.GENRES][TAG.POPULAR]] +\
        [f"{tag}" for tag in datas[TAG.GENRES][TAG.NORMAL]]

    output[TAG.INSTRUMENTS] = \
        [f"{tag}  *" for tag in datas[TAG.INSTRUMENTS][TAG.POPULAR]] +\
        [f"{tag}" for tag in datas[TAG.INSTRUMENTS][TAG.NORMAL]]

    output[TAG.MOODS] = \
        [f"{tag}  *" for tag in datas[TAG.MOODS][TAG.POPULAR]] +\
        [f"{tag}" for tag in datas[TAG.MOODS][TAG.NORMAL]]

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
        [f"{tag}" for tag in datas[TAG.GENRES][TAG.POPULAR]]

    output[TAG.INSTRUMENTS] = \
        [f"{tag}" for tag in datas[TAG.INSTRUMENTS][TAG.POPULAR]]

    output[TAG.MOODS] = \
        [f"{tag}" for tag in datas[TAG.MOODS][TAG.POPULAR]]

    output[TAG.ETC] = output[TAG.GENRES] + \
        output[TAG.INSTRUMENTS]+output[TAG.MOODS]
    output[TAG.TEMPO] = ['Auto', 'Slow', 'Medium', 'Fast']
    output[TAG.DURATION] = ['0:15', '0:30', '1:00']
    return output
