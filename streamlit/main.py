# -*- coding: utf-8 -*-
import os

# streamlit tools
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_space import space
from PIL import Image

# custom
from utils.config import add_logo, delete_another_session_state, set_page
from models.Content import Demo
from constraints import PATH, INFO


set_page()


def guide():
    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)
    delete_another_session_state(' ')

    st.title(INFO.PROJECT_NAME)
    st.divider()

    main_col0, main_col1 = st.columns([2, 6], gap="large")
    with main_col0:
        icon = Image.open(PATH.MAIN_IMAGE).resize((400, 400))
        st.image(icon)
    with main_col1:
        st.markdown(INFO.PROJECT_DETAIL)

    space(lines=3)

    st.markdown("# 데모 버젼")
    st.divider()
    st.markdown("##### ✨ 데모버젼과 함께 음악 생성의 아이디어를 얻어보세요!!")
    space(lines=3)

    # 데모 불러오기
    demos = os.listdir(PATH.DEMO)
    for demo in demos:
        music_paths = [os.path.join(PATH.DEMO, demo, file)
                       for file in os.listdir(os.path.join(PATH.DEMO, demo))]
        Demo(demo, music_paths).set_content()


if __name__ == "__main__":
    guide()
