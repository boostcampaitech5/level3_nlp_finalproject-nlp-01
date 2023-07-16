import json
import requests
import os
import streamlit as st
from PIL import Image

# streamlit tools
from streamlit_tags import st_tags
from streamlit_space import space

# custom
from utils import add_logo, delete_another_session_state, get_music_category
from constraints import PATH, TAG

TITLE = "문서 분석 방식"
button_num = 0

# 문서 분석 컨텐츠 클래스


class TextAnalysisContent():
    def __init__(self, caption, file):
        self.caption = caption
        self.music_file = file

    def set_content(self):
        global button_num

        # css style 추가
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Stylish&display=swap');
        .big-font {
            font-size:22px !important; text-align: center;
            font-family: 'Stylish', sans-serif;
        }
        button {
            height: auto;
            padding-top: 14px !important;
            padding-bottom: 14px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # 첫번째 라인
        self.col00, self.col01 = st.columns([1, 10])
        with self.col00:        # 아이콘 부분
            icon = Image.open(PATH.IMAGE_ICON_PATH).resize((60, 60))
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


# 문서 분석 페이지


def text_analysis():
    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)
    category = get_music_category()

    # Title
    st.title(TITLE)
    st.write("---")

    # 설명
    with st.expander("설명"):
        st.write("사용법 설명")

    # text area
    st.subheader("📔 텍스트 (Texts)")
    text = st.text_area('👉 분석을 진행하고 싶은 텍스트를 입력하세요.', height=300)
    space(lines=1)

    # 사용자 keywords 생성
    etc_data = st_tags(
        label='### ⚙ 그 외 (ETC)',
        text='그 외에 추가하고 싶은 곡 정보를 입력해주세요.',
        value=[],
        suggestions=category[TAG.ETC],
        key="etc_choice")
    space(lines=2)

    col_1, col_2 = st.columns([1, 1], gap="large")

    # 음악 길이
    col_1.subheader('⌛ 길이(Duration)')
    duration = col_1.selectbox(
        label='생성할 음악의 길이를 선택해 주세요',
        options=['0:10', '0:30', '1:00', '1:30', '2:00', '3:00'],
        index=1,
    )

    # 음악 속도
    col_2.subheader('🏇 속도 (Tempo)')
    tempo = col_2.radio('생성할 음악의 빠르기를 선택해 주세요', ['Slow', 'Medium', 'Fast'])

    space(lines=2)

    # 초기화 버튼 / Submit 버튼
    button_cols_1, button_cols_2 = st.columns([14, 2])
    if button_cols_1.button('초기화'):
        if "choice_inputs" in st.session_state:
            del st.session_state['choice_inputs']
            st.experimental_rerun()
    with button_cols_2:
        if st.button("SUBMIT"):
            # duration 파싱
            min, sec = map(int, duration.split(':'))
            duration = min*60 + sec
            inputs = {
                "text": text,
                "etc": etc_data,
                "length": duration,
                "tempo": tempo,
            }

            # requests.post(url="http://127.0.0.1:8000/text_analysis", data=json.dumps(inputs))
            st.session_state['text_state'] = 'result'
            st.experimental_rerun()


# 생성 결과 창


def result_text_analysis(title):
    # 사이드바 로고 추가
    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)

    # 임시 데이터
    audio_file = open(PATH.TEST_MUSIC_PATH, 'rb').read()

    st.title(title)
    st.write("---")

    # summary text area
    st.text_area(label="문서 요약 결과", value=summary_text,
                 height=50, disabled=True)
    space(lines=2)

    # print contents
    music_contents = []
    for _ in range(3):
        music_contents.append(TextAnalysisContent(
            PATH.TEST_CAPTION, audio_file))

    for content in music_contents:
        content.set_content()

    _, button_cols = st.columns([14, 2])
    if button_cols.button("Return"):
        st.session_state['text_state'] = 'execute'
        st.experimental_rerun()


# main

if __name__ == "__main__":

    if 'text_state' not in st.session_state:
        st.session_state['text_state'] = 'execute'

    delete_another_session_state('text_state')

    if st.session_state['text_state'] == 'execute':
        text_analysis()

    else:
        result_text_analysis("🎧 Music Generate Result")
