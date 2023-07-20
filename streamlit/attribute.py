import json

from constraints import PATH, TAG


# api key와 url 정보 불러오기
def get_textunes_secret():
    with open(PATH.SECRET_FILE, 'r') as file:
        data = json.load(file)

    return data
