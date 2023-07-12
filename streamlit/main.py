# -*- coding: utf-8 -*-

# streamlit tools
import streamlit as st
from streamlit_space import space
from PIL import Image

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

    main_col0, _, main_col1 = st.columns([3, 1, 6], gap="small")
    with main_col0:
        icon = Image.open(PATH.IMAGE_ICON_PATH).resize((444, 444))
        st.image(icon)
    with main_col1:
        st.write("프로젝트 간략 소개")

    space(lines=5)

    st.subheader("데모 버젼")
    st.write("---")


guide()
