import base64
from pathlib import Path
import validators

import streamlit as st
from constraints import INFO, PATH
from fastapi import status


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
                background-size: 300px;
                padding-top: {180}px;
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
        if 'state' in state and current_state not in state:
            del st.session_state[state]


def set_page():
    return st.set_page_config(
        page_title=INFO.PROJECT_NAME,
        page_icon=PATH.ICON_PATH,
        layout="wide"
    )
