# -*- coding: utf-8 -*-

# streamlit tools
import streamlit as st

# custom
from utils import add_logo
from constraints import PATH, INFO


st.set_page_config(
    page_title=INFO.PROJECT_NAME,
    page_icon=INFO.PROJECT_ICON,
)


def guide():
    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)

    st.title("가이드")
    st.write("---")

    st.write('설명 추가할 예정')


guide()
