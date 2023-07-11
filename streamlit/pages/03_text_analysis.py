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
<<<<<<< HEAD:streamlit/pages/03_text_analysis.py
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
=======
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
>>>>>>> d9fb528d8a0aa5f73ca45c3766534dfcb2239ddb:streamlit/text_analysis.py
