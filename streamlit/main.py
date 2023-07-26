# -*- coding: utf-8 -*-
import os

# streamlit tools
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_space import space
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

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

    col_0, col_1 = st.columns([3,7])
    with col_0:
        icon = Image.open(PATH.MAIN_IMAGE).resize((480, 360))
        st.image(icon)
    with col_1:
        st.markdown(INFO.PROJECT_DETAIL)
    space(lines=10)

    ## 설명
    col_0, col_1, col_2 = st.columns([7,1,4])
    with col_2:
        icon2 = Image.open(PATH.MAIN_IMAGE).resize((640, 480))
        space(lines=3)
        st.image(image=icon2)
    with col_0:
        st.markdown(INFO.MAIN_SIMPLE_CATEGORY)
        space(lines=2)

        if st.button('Simple-Category 바로가기'):
            switch_page("Simple_Category")
    space(lines=4)
    
    col_0, col_1, col_2 = st.columns([4,1,7])
    with col_2:
        st.markdown(INFO.MAIN_EXTRA_CATEGORY)

        space(lines=2)
        if st.button('Extra-Category 바로가기'):
            switch_page("Extra_Category")
    with col_0:
        space(lines=6)
        icon2 = Image.open(PATH.MAIN_IMAGE).resize((640, 480))
        st.image(image=icon2)
    space(lines=4)

    col_0, col_1, col_2 = st.columns([7,1,4])
    with col_0:
        st.markdown(INFO.MAIN_TEXT_ANALYSIS)
        space(lines=2)
        if st.button('Text-Analysis 바로가기'):
            switch_page('Text_analysis')
    with col_2:
        space(lines=3)
        icon2 = Image.open(PATH.MAIN_IMAGE).resize((640, 480))
        st.image(image=icon2)
    space(lines=10)


    st.markdown("# 데모 버전")
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
