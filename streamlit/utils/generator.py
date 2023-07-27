import numpy as np
from IPython.display import Audio
import openai

from constraints import TAG, SECRET
from utils.attribute import get_simple_category, get_base_category


openai.api_key = SECRET.OPENAI_API


def make_simple_request_json(state):
    category, base_gategory = get_simple_category(), get_base_category()
    key_num = state['key_num']

    # genres
    genres = [base_gategory[TAG.GENRES][genre.split('(')[0].strip()] for genre in category['genres']
              if state[f"{genre}{key_num}"]]
    # instruments
    instruments = [base_gategory[TAG.INSTRUMENTS][instrument.split('(')[0].strip()] for instrument in category['instruments']
                   if state[f"{instrument}{key_num}"]]
    # moods
    moods = [base_gategory[TAG.MOODS][mood.split(
        '(')[0].strip()] for mood in category['moods'] if state[f"{mood}{key_num}"]]

    minute, second = map(int, state[f"{TAG.DURATION}{key_num}"].split(':'))

    return {
        TAG.GENRES: genres,
        TAG.INSTRUMENTS: instruments,
        TAG.MOODS: moods,
        TAG.DURATION: minute*60+second,
        TAG.TEMPO: state[f"{TAG.TEMPO}{key_num}"],
    }


def make_category_request_json(json_dict):
    base_gategory = get_base_category()

    return {
        TAG.GENRES: [base_gategory[TAG.GENRES][t.replace("  *", "").split('(')[0].strip()] for t in json_dict[TAG.GENRES]],
        TAG.INSTRUMENTS: [base_gategory[TAG.INSTRUMENTS][t.replace("  *", "").split('(')[0].strip()] for t in json_dict[TAG.INSTRUMENTS]],
        TAG.MOODS: [base_gategory[TAG.MOODS][t.replace("  *", "").split('(')[0].strip()] for t in json_dict[TAG.MOODS]],
        TAG.ETC: [t.replace("  *", "") for t in json_dict[TAG.ETC]],
        TAG.DURATION: json_dict[TAG.DURATION],
        TAG.TEMPO: json_dict[TAG.TEMPO],
    }


def make_analysis_request_json(json_dict, keywords):
    return {
        TAG.TEXT: keywords.replace('. ', ', '),
        TAG.ETC: [t.replace("  *", "") for t in json_dict[TAG.ETC]],
        TAG.DURATION: json_dict[TAG.DURATION],
        TAG.TEMPO: json_dict[TAG.TEMPO],
    }


def make_audio_data(response):
    res_json = response.json()
    sample_rate = res_json['sample_rate']
    caption = res_json['caption']

    music_output = []

    for res in res_json['music']:
        music_output.append(Audio(np.array(res), rate=sample_rate).data)

    return music_output, caption
