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
def text_analysis(title, category):

    if "text_inputs" not in st.session_state:
        default = {
            TAG.TEXT: " ",
            TAG.ETC: [],
            TAG.DURATION: 1,  # index이므로
            TAG.TEMPO: 1,  # index이므로
        }
    else:
        duration = st.session_state['text_inputs']['duration']
        duration = str(int(duration/60))+':'+str(duration % 60)
        if len(duration) == 3:
            duration += '0'  # 3:0 인경우가 있음
        for i, s in enumerate(category['duration']):
            if s == duration:
                duration = i
                break

        for i, s in enumerate(category['tempo']):
            if s == st.session_state['text_inputs']['tempo']:
                tempo = i
                break

        default = {
            TAG.TEXT: st.session_state['text_inputs']['text'],
            TAG.ETC: st.session_state['text_inputs']['etc'],
            TAG.DURATION: duration,  # index이므로
            TAG.TEMPO: tempo,  # index이므로
        }

    # Title
    st.title(title)
    st.write("---")

    # 설명
    with st.expander("설명"):
        st.write("사용법 설명")
        # To Do: 사용법 내용 채우기

    # text area
    st.subheader("📔 텍스트 (Texts)")
    text = st.text_area(
        '👉 분석을 진행하고 싶은 텍스트를 입력하세요.', 
        height=300, 
        value=default[TAG.TEXT],
        key="text"+st.session_state['key_num'])
    space(lines=1)

    # 사용자 keywords 생성
    etc_data = st_tags(
        label='### ⚙ 그 외 (ETC)',
        text='그 외에 추가하고 싶은 곡 정보를 입력해주세요.',
        suggestions=category[TAG.ETC],
        value=default[TAG.ETC],
        key="etc_choice"+st.session_state['key_num'])
    space(lines=2)

    col_1, col_2 = st.columns([1, 1], gap="large")

    # 음악 길이
    col_1.subheader('⌛ 길이(Duration)')
    duration = col_1.selectbox(
        label='생성할 음악의 길이를 선택해 주세요',
        options=category[TAG.DURATION],
        index=default[TAG.DURATION],
        key="duration"+st.session_state['key_num']
    )

    # 음악 속도
    col_2.subheader('🏇 속도 (Tempo)')
    tempo = col_2.radio(
        label='생성할 음악의 빠르기를 선택해 주세요',
        options=category[TAG.TEMPO],
        index=default[TAG.TEMPO],
        key="tempo"+st.session_state['key_num'])
    space(lines=2)

    # 초기화 버튼 / Submit 버튼
    button_cols_1, button_cols_2 = st.columns([14, 2])
    if button_cols_1.button('초기화'):

        # To DO : 초기화 버튼 작업 진행
        if "text_inputs" in st.session_state:
            del st.session_state['text_inputs']

        # key값을 변경 -> 값의 초기화하고 새로고침을 만들기 위해 key값을 다르게 설정
        if st.session_state['key_num'] == TAG.ONE:
            st.session_state['key_num'] = TAG.TWO
        else:
            st.session_state['key_num'] = TAG.ONE

        st.experimental_rerun()
        

    with button_cols_2:
        if st.button("SUBMIT"):
            # duration 파싱
            min, sec = map(int, duration.split(':'))
            duration = min*60 + sec
            inputs = {
                "text": text,
                "etc": etc_data,
                "duration": duration,
                "tempo": tempo,
            }

            # res = requests.post(url="http://127.0.0.1:8000/text_analysis", data=json.dumps(inputs))
            st.session_state['text_inputs'] = inputs
            st.session_state['text_state'] = 'submit'
            st.experimental_rerun()


# 제출 화면
def submit_text_analysis(title, category):
    
    if "text_inputs" not in st.session_state:
        default = {
            TAG.TEXT: " ", # []로 설정하면 []가 적혀있음
            TAG.ETC: [],
            TAG.DURATION: 1,  # index이므로
            TAG.TEMPO: 1,  # index이므로
        }
    else:
        duration = st.session_state['text_inputs']['duration']
        duration = str(int(duration/60))+':'+str(duration % 60)
        if len(duration) == 3:
            duration += '0'  # 3:0 인경우가 있음
        for i, s in enumerate(category['duration']):
            if s == duration:
                duration = i
                break

        for i, s in enumerate(category['tempo']):
            if s == st.session_state['text_inputs']['tempo']:
                tempo = i
                break

        default = {
            TAG.TEXT: st.session_state['text_inputs']['text'],
            TAG.ETC: st.session_state['text_inputs']['etc'],
            TAG.DURATION: duration,  # index이므로
            TAG.TEMPO: tempo,  # index이므로
        }

    # Title
    st.title(title)
    st.write("---")

    # 설명
    with st.expander("설명"):
        st.write("사용법 설명")
        # To Do: 사용법 내용 채우기

    # text area
    st.subheader("📔 텍스트 (Texts)")
    text = st.text_area(
        '👉 분석을 진행하고 싶은 텍스트를 입력하세요.', 
        height=300, 
        value=default[TAG.TEXT],
        key="text"+st.session_state['key_num'],
        disabled=True)
    space(lines=1)

    # 사용자 keywords 생성
    st.subheader('⚙ 기타 (ETC)')
    etc = st.multiselect(
        label='생성할 음악의 추가정보를 입력해 주세요',
        options=default[TAG.ETC],
        default=default[TAG.ETC],
        disabled=True)
    space(lines=2)

    col_1, col_2 = st.columns([1, 1], gap="large")

    # 음악 길이
    col_1.subheader('⌛ 길이(Duration)')
    duration = col_1.selectbox(
        label='생성할 음악의 길이를 선택해 주세요',
        options=category[TAG.DURATION],
        index=default[TAG.DURATION],
        key="duration"+st.session_state['key_num'],
        disabled=True
    )

    # 음악 속도
    col_2.subheader('🏇 속도 (Tempo)')
    tempo = col_2.radio(
        label='생성할 음악의 빠르기를 선택해 주세요',
        options=category[TAG.TEMPO],
        index=default[TAG.TEMPO],
        key="tempo"+st.session_state['key_num'],
        disabled=True)
    space(lines=2)

    with st.spinner('음악을 생성중입니다...'):
        res = requests.post(url = "http://127.0.0.1:8000/text_analysis", data = json.dumps(st.session_state['text_inputs']))
    
    st.session_state['res'] = res
    st.session_state['text_state'] = 'result'
    st.experimental_rerun()

# 생성 결과 창
def result_text_analysis(title):

    # 임시 데이터
    audio_file = open(PATH.TEST_MUSIC_PATH, 'rb').read()

    st.title(title)
    st.write("---")

    # summary text area
    st.text_area(label="문서 요약 결과", value=TAG.SUMMARY_TEXT,
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

    
    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)       # 사이드에 로고 추가
    category = get_music_category()          # 각 카테고리의 정보 가져오기

    if 'text_state' not in st.session_state:
        st.session_state['text_state'] = 'execute'

    # 초기화를 위한 key state생성
    if 'key_num' not in st.session_state:
        st.session_state['key_num'] = TAG.ONE

    delete_another_session_state('text_state')

    if st.session_state['text_state'] == 'execute':
        text_analysis(TITLE, category=category)

    elif st.session_state['text_state'] == 'submit':
        submit_text_analysis(TITLE, category=category)

    else:
        result_text_analysis("🎧 Music Generate Result")
