# -*- coding: utf-8 -*-

import os

# streamlit tools
import streamlit as st
from streamlit_tags import st_tags
from choice_category import choice_category
from text_analysis import text_analysis
from guide import guide


BASE_PATH = "" # 내 로컬에서 작업할 경우 오류가 나서 일단 없앰
SIDEBAR_IMAGE_PATH = os.path.join(BASE_PATH, "assets/crying_frog.png")
APP_WORK = ["가이드", "카테고리 선택 방식", "문서 분석 방식"]


st.sidebar.image(SIDEBAR_IMAGE_PATH)
page = st.sidebar.radio("원하는 서비스를 선택하세요", APP_WORK)


def main():
    # To DO : 웹페이지 UI 개선

    # page 선택에 따라 함수 호출
    if page == APP_WORK[0]:
        guide(APP_WORK[0])
    elif page == APP_WORK[1]:
        choice_category(APP_WORK[1])
    elif page == APP_WORK[2]:
        text_analysis(APP_WORK[2])
    


main()      # 메인 실행문
