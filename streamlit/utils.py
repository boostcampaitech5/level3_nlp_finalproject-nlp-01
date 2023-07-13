import json
import base64
from pathlib import Path

import streamlit as st
import validators

from constraints import PATH, TAG


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


def get_music_category():
    with open(PATH.DATA_PATH, 'r', encoding='utf-8') as f:
        datas = json.load(f)

    datas[TAG.GENRES] = [tag.title() for tag in datas[TAG.GENRES]]
    datas[TAG.INSTRUMENTS] = [tag.title() for tag in datas[TAG.INSTRUMENTS]]
    datas[TAG.MOODS] = [tag.title() for tag in datas[TAG.MOODS]]

    datas[TAG.ETC] = datas[TAG.GENRES]+datas[TAG.INSTRUMENTS]+datas[TAG.MOODS]
    return datas
