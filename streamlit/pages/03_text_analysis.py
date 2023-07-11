import json
import requests
import streamlit as st
from streamlit_tags import st_tags


# 문서 분석 방식

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


def text_analysis():

    st.title("문서 분석 방식")
    st.write("---")

    with st.expander("# Custom"):

        # multiselect
        st.write('### 장르 (Genre)')
        options_0 = st.multiselect(
            label='🎼 배경음악의 장르를 정해주세요.',
            options=['Green', 'Yellow', 'Red', 'Blue'],
            default=[])

        st.write('### 악기 (Musical Instruments)')
        options_1 = st.multiselect(
            label='🥁 배경음악의 악기를 정해주세요.',
            options=['Green', 'Yellow', 'Red', 'Blue'],
            default=[])

        st.write('### 분위기 (Mood)')
        options_2 = st.multiselect(
            label='📣 배경음악의 분위기를 정해주세요.',
            options=['Green', 'Yellow', 'Red', 'Blue'],
            default=[])

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
    
    # text area
    text = st.text_area('분석을 진행하고 싶은 텍스트를 입력하세요 👉')
    
    if st.button("SUBMIT"):
        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        min, sec = map(int,options_4.split(':'))
        options_4 = min*60 + sec
        inputs = {
            "genre": options_0,
            "instrument": options_1,
            "mood": options_2,
            "etc": options_3,
            "text": text,
            "time": options_4,
            "tempo": options_5,
        }
        st.write(inputs)
        requests.post(url = "http://127.0.0.1:8000/text_analysis", data = json.dumps(inputs))

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

    col_1, col_2 = st.columns([4,1])

    for i, w in enumerate(inputs['wav']):
        col_1.audio(data=w)
        col_2.download_button(label=f"Download{i+1}", data=w)

    if st.button("Return"):
        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        requests.get(url = "http://127.0.0.1:8000/return/choice_category")


# 임시 input
inputs = {
    'captions':['1', '2', '3'],
    'wav': [create_exam_binary(), create_exam_binary(), create_exam_binary(), create_exam_binary()]
    }
result_choice_category('Result', inputs)


text_analysis()