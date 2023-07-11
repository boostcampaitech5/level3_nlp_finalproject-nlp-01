import json
import requests
import streamlit as st
import numpy as np


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


# 카테고리 선택 방식 결과 페이지


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
        st.write("Return")


# 임시 input
inputs = {
    'captions': ['1', '2', '3'],
    'wav': [create_exam_binary(), create_exam_binary(), create_exam_binary(), create_exam_binary()]
}
result_choice_category('Result', inputs)
