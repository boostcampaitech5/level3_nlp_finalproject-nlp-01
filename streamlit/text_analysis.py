import json
import requests
import streamlit as st

# streamlit tools
from streamlit_tags import st_tags
from streamlit_space import space

# custom
from utils import get_component

ETC = get_component("etc")

# 문서 분석 방식


def text_analysis(title):

    st.title(title)
    st.write("---")

    # 음악 길이 지정
    st.subheader("재생 길이 (Length)")
    options_1 = st.selectbox(
        label='⌛ 생성할 음악의 시간을 정해주세요. ',
        index=2,
        options=['0 : 10', '0 : 20', '0 : 30', '0 : 40',
                 '1 : 00', '1 : 30', '2 : 00', '3 : 00'],
    )
    space(lines=2)

    # 사용자 keywords 생성
    options_2 = st_tags(
        label='### 그 외 (ETC)',
        text='그 외에 추가하고 싶은 곡 정보를 입력해주세요.',
        value=[],
        suggestions=ETC,
        key="etc_choice")
    space(lines=2)
    # text area
    space(lines=1)
