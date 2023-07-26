import numpy as np
from IPython.display import Audio
import openai

from constraints import TAG, SECRET


openai.api_key = SECRET.OPENAI_API


def make_simple_request_json(category, check_dict):

    key_num = check_dict['key_num']

    # genres
    genres = [genre for genre in category['genres'] if check_dict[f"{genre}{key_num}"]]
    # instruments
    instruments = [instrument for instrument in category['instruments']
                   if check_dict[f"{instrument}{key_num}"]]
    # moods
    moods = [mood for mood in category['moods'] if check_dict[f"{mood}{key_num}"]]

    minute, second = map(int, check_dict[f"{TAG.DURATION}{key_num}"].split(':'))

    return {
        TAG.GENRES: genres,
        TAG.INSTRUMENTS: instruments,
        TAG.MOODS: moods,
        TAG.DURATION: minute*60+second,
        TAG.TEMPO: check_dict[f"{TAG.TEMPO}{key_num}"],
    }


def make_category_request_json(json_dict):
    return {
        TAG.GENRES: [t.replace("  *", "") for t in json_dict[TAG.GENRES]],
        TAG.INSTRUMENTS: [t.replace("  *", "") for t in json_dict[TAG.INSTRUMENTS]],
        TAG.MOODS: [t.replace("  *", "") for t in json_dict[TAG.MOODS]],
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
