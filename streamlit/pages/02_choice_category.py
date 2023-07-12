import json
import requests
import numpy as np
import streamlit as st
from streamlit_tags import st_tags
from streamlit_space import space
from PIL import Image


# custom
from utils import add_logo
from constraints import PATH

# 카테고리 선택 방식 Page
button_num = 0


class CategoryChoiceContent():
    def __init__(self, file):
        self.music_file = file

    def set_content(self):
        global button_num

        # 첫번째 라인
        col0, col1, col2 = st.columns([2, 8, 2])
        with col0:        # 아이콘 부분
            icon = Image.open(PATH.IMAGE_ICON_PATH).resize((100, 100))
            st.image(icon)
        with col1:        # 음악 재생 부분
            st.audio(self.music_file, format='audio/ogg')
        with col2:
            music_caption = '_'.join(self.caption)
            st.download_button(
                label=":blue[DOWNLOAD]",        # 버튼 라벨 텍스트
                key=f"button{str(button_num)}",
                data=self.music_file,
                file_name=f"{music_caption}_music.wav"
            )
            button_num += 1     # 버튼은 key값을 지정해야 하기때문에 임의로 Key를 지정
        space(lines=2)      # 컨텐츠 구분을 짓기 위한 개행 처리


def choice_category():
    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)

    st.title("카테고리 선택 방식")
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

    options_4 = st.selectbox(
        label='생성할 음악의 시간을 정해주세요',
        options=['0:10', '0:30', '1:00', '1:30', '2:00', '3:00'],
    )

    options_5 = st.radio('음악의 빠르기를 선택해 주세요', ['slow', 'normal', 'fast'])

    if st.button("SUBMIT"):
        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        min, sec = map(int, options_4.split(':'))
        options_4 = min*60 + sec
        inputs = {
            "genre": options_0,
            "instrument": options_1,
            "mood": options_2,
            "etc": options_3,
            "time": options_4,
            "tempo": options_5,
        }
        st.write(inputs)
        # res = requests.post(url = "http://127.0.0.1:8000/choice_category", data = json.dumps(inputs))
        st.session_state['state'] = 'result'
        st.experimental_rerun()


# 결과 페이지

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

    if st.button("Return"):
        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        st.session_state['state'] = 'execute'
        st.experimental_rerun()


# main


if __name__ == "__main__":

    if 'state' not in st.session_state:
        st.session_state['state'] = 'execute'

    if st.session_state['state'] == 'execute':
        choice_category()

    else:
        # 임시 input 생성
        inputs = {
            'captions': ['1', '2', '3'],
            'wav': [create_exam_binary(), create_exam_binary(), create_exam_binary(), create_exam_binary()]
        }

        result_choice_category('Result', inputs)

    del st.session_state['state']
