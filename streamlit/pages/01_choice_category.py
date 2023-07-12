import json
import requests
import numpy as np
import streamlit as st
from streamlit_tags import st_tags
from utils import add_logo
from streamlit_space import space
from constraints import PATH


# 카테고리 선택 페이지
def choice_category(title, options):

    st.title(title)
    st.write("---")

    # multiselect
    st.subheader('🎼 장르 (Genre)')
    genre = st.multiselect(
        label='생성할 음악의 장르를 선택해 주세요.',
        options=['Green', 'Yellow', 'Red', 'Blue'],
        default=['Red'])
    space(lines=1)
    
    st.subheader('🥁 악기 (Musical Instruments)')
    Instruments = st.multiselect(
        label='생성할 음악의 악기를 선택해 주세요.',
        options=['Green', 'Yellow', 'Red', 'Blue'],
        default=['Yellow'])
    space(lines=1)

    st.subheader('📣 분위기 (Mood)')
    mood = st.multiselect(
        label='생성할 음악의 분위기를 선택해 주세요.',
        options=['Green', 'Yellow', 'Red', 'Blue'],
        default=['Green'])
    space(lines=1)

    # 사용자 keywords 생성
    etc = st_tags(
        label='### 기타 (ETC)',
        text='생성할 음악의 추가정보를 입력해 주세요',
        value=[],
        suggestions=['Green', 'Yellow', 'Red', 'Blue'],
        key="etc_choice")
    space(lines=1)

    col_1, col_2 = st.columns([1,1])

    col_1.subheader('⌛ 길이(Duration)')
    duration = col_1.selectbox(
        label='생성할 음악의 길이를 선택해 주세요',
        options=['0:10', '0:30', '1:00', '1:30', '2:00', '3:00'],
        index=1,
    )

    col_2.subheader('속도 (Tempo)')
    tempo = col_2.radio('생성할 음악의 빠르기를 선택해 주세요', ['Slow', 'Medium', 'Fast'])

    _, button_cols = st.columns([14, 2])
    if button_cols.button("Submit"):
        
        # duration 파싱
        min, sec = map(int, duration.split(':'))
        duration = min*60 + sec

        # input 생성
        inputs = {
            "genre": genre,
            "instruments": Instruments,
            "mood": mood,
            "etc": etc,
            "duration": duration,
            "tempo": tempo,
        }

        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        # res = requests.post(url = "http://127.0.0.1:8000/choice_category", data = json.dumps(inputs))
        
        # session_state 변경 -> result 페이지로 이동
        st.session_state['state'] = 'result'
        st.experimental_rerun()


# 임시 examp생성
def create_exam_audio():
    sample_rate = 44100  # 44100 samples per second
    seconds = 2  # Note duration of 2 seconds

    frequency_la = 440  # Our played note will be 440 Hz

    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, seconds * sample_rate, False)

    # Generate a 440 Hz sine wave
    note_la = np.sin(frequency_la * t * 2 * np.pi)
    return note_la

def create_exam_binary():
    binary_contents = b'example content'
    return binary_contents


# 결과 페이지
def result_choice_category(title, inputs):

    st.title(title)
    st.write("---")

    st.write("### Caption")
    captions = st.multiselect(
        label='선택된 Caption',
        options=inputs['captions'],
        default=inputs['captions'],
        disabled=True
    )

    col_1, col_2 = st.columns([4, 1])

    for i, w in enumerate(inputs['wav']):
        col_1.audio(data=w)
        col_2.download_button(label=f"Download{i+1}", data=w)

    _, button_cols = st.columns([14, 2])

    if button_cols.button("Return"):
        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        st.session_state['state'] = 'execute'
        st.experimental_rerun()


# main


if __name__ == "__main__":

    if 'state' not in st.session_state:
        st.session_state['state'] = 'execute'

    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)

    if st.session_state['state'] == 'execute':
        choice_category('카테고리 선택', None)

    else:
        # 임시 input 생성
        inputs = {
            'captions': ['1', '2', '3'],
            'wav': [create_exam_binary(), create_exam_binary(), create_exam_binary(), create_exam_binary()]
        }
        result_choice_category('Result', inputs)

    del st.session_state['state'] # 페이지에서 이동할 경우 state초기화
