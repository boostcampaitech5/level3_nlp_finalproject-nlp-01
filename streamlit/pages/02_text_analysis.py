import json
import requests
import os
import numpy as np
import streamlit as st
from pathlib import Path
from PIL import Image

# streamlit tools
from streamlit_tags import st_tags
from streamlit_space import space

# custom
from utils import get_component, add_logo
from constraints import PATH

ETC = get_component("etc")

TITLE = "문서 분석 방식"
TEST_MUSIC_PATH = os.path.join(PATH.BASE_PATH, "assets", "test_music.wav")
TEST_CAPTION = ["Orchestral", "With a strings", "Cinematic", "Slow bpm"]
button_num = 0


class TextAnalysisContent():
    def __init__(self, caption, file):
        self.caption = caption
        self.music_file = file

    def set_content(self):
        global button_num

        st.markdown("""
        <style>
        .big-font {
            font-size:20px !important; text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

        # 첫번째 라인
        self.col00, self.col01 = st.columns([1, 10])
        with self.col00:        # 아이콘 부분
            icon = Image.open(PATH.IMAGE_ICON_PATH)
            st.image(icon)
        with self.col01:        # 캡션 부분
            caption = ', '.join(self.caption)
            st.markdown(
                f'<p class="big-font">{caption}</p>', unsafe_allow_html=True)

        # 두번째 라인
        self.col10, self.col11 = st.columns([10, 2])
        with self.col10:        # 음악 재생 부분
            st.audio(self.music_file, format='audio/ogg')
        with self.col11:        # 다운로드 부분
            music_caption = '_'.join(self.caption)
            st.download_button(
                label=":blue[DOWNLOAD]",        # 버튼 라벨 텍스트
                key=f"button{str(button_num)}",
                data=self.music_file,
                file_name=f"{music_caption}_music.wav"
            )
            button_num += 1     # 버튼은 key값을 지정해야 하기때문에 임의로 Key를 지정
        space(lines=2)      # 컨텐츠 구분을 짓기 위한 개행 처리


# 문서 분석 방식
TITLE = "문서 분석 방식"


def text_analysis():
    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)

    title_cols1, title_cols2 = st.columns([14, 2])
    with title_cols1:
        st.title(TITLE)
    with title_cols2:
        ta_info = st.button(label='?')

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
            # requests.post(url="http://127.0.0.1:8000/text_analysis", data=json.dumps(inputs))
            st.session_state['state'] = 'result'
            st.experimental_rerun()


def result_text_analysis():
    summary_text = "Orchestral, with a strings, cinematic, slow bpm"
    audio_file = open(TEST_MUSIC_PATH, 'rb').read()

    st.title(TITLE)
    st.write("---")

    # summary text area
    st.text_area(label="문서 요약 결과", value=summary_text,
                 height=50, disabled=True)
    space(lines=2)

    # print contents
    music_contents = []
    for _ in range(5):
        music_contents.append(TextAnalysisContent(TEST_CAPTION, audio_file))

    for content in music_contents:
        content.set_content()

    if st.button("Return"):
        st.session_state['state'] = 'result'
        st.experimental_rerun()


# main


if __name__ == "__main__":

    if 'state' not in st.session_state:
        st.session_state['state'] = 'execute'

    if st.session_state['state'] == 'execute':
        text_analysis()

    else:
        result_text_analysis()

    del st.session_state['state']
