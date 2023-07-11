import json
import requests
import streamlit as st
from streamlit_tags import st_tags



# 카테고리 선택 방식 Page


def choice_category(title):

    st.title(title)
    st.write("---")

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
        inputs = {
            "genre": options_0,
            "instrument": options_1,
            "mood": options_2,
            "etc": options_3
        }
        st.write(inputs)
