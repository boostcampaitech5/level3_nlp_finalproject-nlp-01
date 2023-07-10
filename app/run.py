# -*- coding: utf-8 -*-

import os

# streamlit tools
import streamlit as st
from streamlit_tags import st_tags
BASE_PATH = "./app"
SIDEBAR_IMAGE_PATH = os.path.join(BASE_PATH, "assets/crying_frog.png")
APP_WORK = ["카테고리 선택 방식", "문서 분석 방식"]

st.sidebar.image(SIDEBAR_IMAGE_PATH)
page = st.sidebar.radio("원하는 서비스를 선택하세요", APP_WORK)
# 카테고리 선택 방식

def choice_category():

    # multiselect
    st.write('### 장르 (Genre)')
    options_0 = st.multiselect(
        label='🎼 배경음악의 장르를 정해주세요.',
        options=['Green', 'Yellow', 'Red', 'Blue'],
        default=['Red'])

    st.write('### 악기 (Musical Instruments)')
    options_1 = st.multiselect(
        label='🥁 배경음악의 악기를 정해주세요.',
        options=['Green', 'Yellow', 'Red', 'Blue'],
        default=['Yellow'])

    st.write('### 분위기 (Mood)')
    options_2 = st.multiselect(
        label='📣 배경음악의 분위기를 정해주세요.',
        options=['Green', 'Yellow', 'Red', 'Blue'],
        default=['Green'])

    # 사용자 keywords 생성
    options_3 = st_tags(
        label='### 그 외 (ETC)',
        text='그 외에 추가하고 싶은 곡 정보를 입력해주세요.',
        value=['Blue'],
        suggestions=['Green', 'Yellow', 'Red', 'Blue'],
        key="etc_choice")

    if st.button("SUBMIT"):
        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        st.write(options_0+options_1+options_2+options_3)
# 문서 분석 방식

def text_analysis():
    # text area
    text = st.text_area('분석을 진행하고 싶은 텍스트를 입력하세요 👉')
    if st.button("SUBMIT"):
        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        st.write(text)
