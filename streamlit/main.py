# -*- coding: utf-8 -*-

import os

# streamlit tools
import streamlit as st


BASE_PATH = "streamlit"  # 내 로컬에서 작업할 경우 오류가 나서 일단 없앰
SIDEBAR_IMAGE_PATH = os.path.join(BASE_PATH, "assets/sidebar_logo.png")
APP_WORK = ["가이드", "카테고리 선택 방식", "문서 분석 방식"]


st.sidebar.image(SIDEBAR_IMAGE_PATH)
# page = st.sidebar.radio("원하는 서비스를 선택하세요", APP_WORK)
