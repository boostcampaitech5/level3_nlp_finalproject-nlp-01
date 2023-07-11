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


def text_analysis():

    st.title("문서 분석 방식")
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
    st.subheader("텍스트 (Texts)")
    text = st.text_area('👉 분석을 진행하고 싶은 텍스트를 입력하세요.')
    space(lines=1)
    # Submit button
    _, button_cols = st.columns([14, 2])
    with button_cols:
        if st.button("SUBMIT"):
            # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
            min, sec = map(int, options_1.split(':'))
            length = min*60 + sec
            inputs = {
                "length": length,
                "etc": options_2,
                "text": text,
            }
            st.write(inputs)
            requests.post(url="http://127.0.0.1:8000/text_analysis",
                          data=json.dumps(inputs))



text_analysis()