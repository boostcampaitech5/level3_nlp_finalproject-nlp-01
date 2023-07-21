import json
import base64
from pathlib import Path
import numpy as np
from IPython.display import Audio
import urllib.request
import urllib
from googletrans import Translator  # googletrans==3.1.0a0

import streamlit as st
import validators
import openai

from constraints import PATH, TAG, SECRET

openai.api_key = SECRET.OPENAI_API


def add_logo(logo_url: str, height: int = 120):
    """Add a logo (from logo_url) on the top of the navigation page of a multipage app.
    Taken from https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/6

    The url can either be a url to the image, or a local path to the image.

    Args:
        logo_url (str): URL/local path of the logo
    """

    if validators.url(logo_url) is True:
        logo = f"url({logo_url})"
    else:
        logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                background-size: 250px;
                padding-top: {height+50}px;
                margin-top: 50px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def delete_another_session_state(current_state: str) -> None:
    """session_state 삭제.

    현제 페이지의 session_state의 state만 남기고, 다른 페이지의 state를 삭제합니다.

    Args:
        remain_state (str): 현제 페이지의 session_state
    """
    for state in st.session_state.to_dict():
        if 'state' in state and state != current_state:
            del st.session_state[state]


def make_simple_request_json(category, check_dict):
    # genres
    genres = [genre for genre in category['genres'] if check_dict[f"{genre}1"]]
    # instruments
    instruments = [instrument for instrument in category['instruments']
                   if check_dict[f"{instrument}1"]]
    # moods
    moods = [mood for mood in category['moods'] if check_dict[f"{mood}1"]]

    minute, second = map(int, check_dict[f"{TAG.DURATION}1"].split(':'))

    return {
        TAG.GENRES: genres,
        TAG.INSTRUMENTS: instruments,
        TAG.MOODS: moods,
        TAG.ETC: [t.replace("  *", "") for t in check_dict[f"{TAG.ETC}1"]],
        TAG.DURATION: minute*60+second,
        TAG.TEMPO: check_dict[f"{TAG.TEMPO}1"],
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


def google_trans(text):
    translator = Translator()
    result = translator.translate(text, src='ko', dest='en')
    return result.text


def create_caption(res):
    genre, summary = res['genre'], res['summary']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Based on the contents of {genre} as genre and {summary} as story, please create a caption that expresses musical elements such as genre, instrument, emotion, and song style.\
             Just like the following sentence: Meditative song, calming and soothing, with flutes and guitars. The music is slow, with a focus on creating a sense of peace and tranquility."},
            {"role": "assistant", "content": "Meditative song, calming and soothing, with flutes and guitars. The music is slow, with a focus on creating a sense of peace and tranquility."},
        ]
    )

    return response['choices'][0]['message']['content']
