import json
import requests
import streamlit as st
from fastapi import status

# streamlit tools
from streamlit_tags import st_tags
from streamlit_space import space

# custom
from utils.attribute import get_music_category
from utils.config import add_logo, delete_another_session_state, set_page
from utils.log import print_error
from utils.generator import make_analysis_request_json, make_audio_data
from utils.api import google_trans, create_gpt_caption
from models.Content import MusicContent
from constraints import INFO, PATH, TAG, SECRET, COMPONENT

st.session_state[TAG.BUTTON_NUM] = 0
set_page()
add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)


# 문서 분석 페이지
def text_analysis(title, category):

    if TAG.TEXT_INPUTS not in st.session_state:
        default = COMPONENT.DEFAULT_TEXT
    else:
        duration = st.session_state[TAG.TEXT_INPUTS][TAG.DURATION]
        duration = str(int(duration/60))+':'+str(duration % 60)
        if len(duration) == 3:
            duration += '0'  # 3:0 인경우가 있음
        for i, s in enumerate(category[TAG.DURATION]):
            if s == duration:
                duration = i
                break
        
        # [] 인 경우, Auto
        if st.session_state[TAG.TEXT_INPUTS][TAG.TEMPO] == []:
                st.session_state[TAG.TEXT_INPUTS][TAG.TEMPO] = 'Auto'

        for i, s in enumerate(category[TAG.TEMPO]):
            if s == st.session_state[TAG.TEXT_INPUTS][TAG.TEMPO]:
                tempo = i
                break

        default = {
            TAG.TEXT: st.session_state[TAG.TEXT_INPUTS][TAG.TEXT],
            TAG.ETC: st.session_state[TAG.TEXT_INPUTS][TAG.ETC],
            TAG.DURATION: duration,  # index이므로
            TAG.TEMPO: tempo,  # index이므로
        }

    # 오류 발생
    if st.session_state[TAG.TEXT_RES_STATE] != status.HTTP_200_OK:
        st.toast(print_error(st.session_state[TAG.TEXT_RES_STATE]))
        st.session_state[TAG.SIMPLE_RES_STATE] = 200


    # Title
    st.title(title)
    st.divider()

    # 설명
    st.markdown("""
        <style>
        div[data-testid="stExpander"] div[role="button"] p {
            font-size: 24px;
            font-weight:bold;
        }</style>""", unsafe_allow_html=True)
    with st.expander(TAG.GUIDE_HEADER):
        st.markdown(INFO.TEXT_ANALYSIS_GUIDE)
    space(lines=2)

    # text area
    st.subheader(TAG.TEXT_HEADER)
    text = st.text_area(
        TAG.TEXT_DESCRIPTION,
        height=300,
        value=default[TAG.TEXT],
        key="text"+st.session_state['key_num'])
    space(lines=1)

    # 사용자 keywords 생성
    etc_data = st_tags(
        label=TAG.ETC_HEADER,
        text=TAG.ETC_DESCRIPTION,
        suggestions=category[TAG.ETC],
        value=default[TAG.ETC],
        key="etc_choice"+st.session_state['key_num'])
    st.write('※　ex) calm music, smooth jazz, Dark, Funny music, Children music, christmas music')
    space(lines=2)

    col_1, col_2 = st.columns([1, 1], gap="large")

    # 음악 길이
    col_1.subheader(TAG.DURATION_HEADER)
    duration = col_1.selectbox(
        label=TAG.DURATION_DESCRIPTION,
        options=category[TAG.DURATION],
        index=default[TAG.DURATION],
        key="duration"+st.session_state['key_num']
    )

    # 음악 속도
    col_2.subheader(TAG.TEMPO_HEADER)
    tempo = col_2.radio(
        label=TAG.TEMPO_DESCRIPTION,
        options=category[TAG.TEMPO],
        index=default[TAG.TEMPO],
        key="tempo"+st.session_state['key_num'])
    space(lines=2)

    # 초기화 버튼 / Submit 버튼
    button_cols_1, button_cols_2 = st.columns([14, 2])
    if button_cols_1.button('초기화'):

        # To DO : 초기화 버튼 작업 진행
        if TAG.TEXT_INPUTS in st.session_state:
            del st.session_state[TAG.TEXT_INPUTS]

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
                TAG.TEXT: text,
                TAG.ETC: etc_data,
                TAG.DURATION: duration,
                TAG.TEMPO: tempo,
            }

            if inputs[TAG.TEXT] == [] and inputs[TAG.ETC] == []:
                st.toast('입력을 확인해 주세요')

            else:
                # tempo가 Auto인 경우
                if inputs[TAG.TEMPO] == 'Auto':
                    inputs[TAG.TEMPO] = []
                st.session_state[TAG.TEXT_INPUTS] = inputs
                st.session_state[TAG.TEXT_STATE] = 'submit'
                st.experimental_rerun()


# 제출 화면
def submit_text_analysis(title, category):

    if TAG.TEXT_INPUTS not in st.session_state:
        default = COMPONENT.DEFAULT_TEXT
    else:
        duration = st.session_state[TAG.TEXT_INPUTS][TAG.DURATION]
        duration = str(int(duration/60))+':'+str(duration % 60)
        if len(duration) == 3:
            duration += '0'  # 3:0 인경우가 있음
        for i, s in enumerate(category[TAG.DURATION]):
            if s == duration:
                duration = i
                break
        
        # [] 인 경우, Auto
        if st.session_state[TAG.TEXT_INPUTS][TAG.TEMPO] == []:
                st.session_state[TAG.TEXT_INPUTS][TAG.TEMPO] = 'Auto'

        for i, s in enumerate(category[TAG.TEMPO]):
            if s == st.session_state[TAG.TEXT_INPUTS][TAG.TEMPO]:
                tempo = i
                break

        default = {
            TAG.TEXT: st.session_state[TAG.TEXT_INPUTS][TAG.TEXT],
            TAG.ETC: st.session_state[TAG.TEXT_INPUTS][TAG.ETC],
            TAG.DURATION: duration,  # index이므로
            TAG.TEMPO: tempo,  # index이므로
        }

    # Title
    st.title(title)
    st.divider()

    # 설명
    st.markdown("""
        <style>
        div[data-testid="stExpander"] div[role="button"] p {
            font-size: 24px;
            font-weight:bold;
        }</style>""", unsafe_allow_html=True)
    with st.expander(TAG.GUIDE_HEADER):
        st.markdown(INFO.TEXT_ANALYSIS_GUIDE)
    space(lines=2)

    # text area
    st.subheader(TAG.TEXT_HEADER)
    text = st.text_area(
        TAG.TEXT_DESCRIPTION,
        height=300,
        value=default[TAG.TEXT],
        key="text"+st.session_state['key_num'],
        disabled=True)
    space(lines=1)

    # 사용자 keywords 생성
    st.subheader(TAG.ETC_HEADER[3:])
    etc = st.multiselect(
        label=TAG.ETC_DESCRIPTION,
        options=default[TAG.ETC],
        default=default[TAG.ETC],
        disabled=True)
    st.write('※　ex) calm music, smooth jazz, Dark, Funny music, Children music, christmas music')
    space(lines=2)

    col_1, col_2 = st.columns([1, 1], gap="large")

    # 음악 길이
    col_1.subheader(TAG.DURATION_HEADER)
    duration = col_1.selectbox(
        label=TAG.DURATION_DESCRIPTION,
        options=category[TAG.DURATION],
        index=default[TAG.DURATION],
        key="duration"+st.session_state['key_num'],
        disabled=True
    )

    # 음악 속도
    col_2.subheader(TAG.TEMPO_HEADER)
    tempo = col_2.radio(
        label=TAG.TEMPO_DESCRIPTION,
        options=category[TAG.TEMPO],
        index=default[TAG.TEMPO],
        key="tempo"+st.session_state['key_num'],
        disabled=True)
    space(lines=2)

    with st.spinner(TAG.REQUEST_MESSAGE):
        res = requests.post(url=SECRET.TEXT_ANALYSIS_URL,
                            data=json.dumps(st.session_state[TAG.TEXT_INPUTS]))

        print(">> 문서 분석 완료 : ", res)
        keywords = create_gpt_caption(res.json())
        my_json = make_analysis_request_json(
            st.session_state[TAG.TEXT_INPUTS], keywords)

        # etc (custom keyword) 번역
        #TODO origin 다시 사용해야함
        # 실행 : 안녕하세요 -> 결과 : hello (목표 -> 결과 : '안녕하세요' 유지)
        trans_tmp = my_json[TAG.ETC]
        trans_tmp = '@^'.join(trans_tmp)
        trans_tmp = google_trans(trans_tmp)
        trans_tmp = trans_tmp.split('@^')
        my_json[TAG.ETC] = [i.strip() for i in trans_tmp]

        res = requests.post(SECRET.MUSICGEN_ANALYSIS_URL, json=my_json)

        st.session_state[TAG.TEXT_RES_STATE] = res.status_code

        if res.status_code != status.HTTP_200_OK:
            st.session_state[TAG.TEXT_RES_STATE] = 'execute'
            st.experimental_rerun()

        else:
            print(">> 음악 생성 완료 : ", res)
            audio_files, caption = make_audio_data(res)
            st.session_state[TAG.AUDIOFILE] = {
                TAG.AUDIOS: audio_files, TAG.CAPTIONS: caption}

            st.session_state['res'] = res
            st.session_state[TAG.TEXT_STATE] = 'result'
            st.experimental_rerun()

# 생성 결과 창


def result_text_analysis(title, inputs):
    st.markdown("""
        <style>
            .stMultiSelect [data-baseweb=select] span{
                max-width: 50000px;
                font-size: 1rem;
            }
        </style>
        """, unsafe_allow_html=True)
    caption = inputs[TAG.CAPTIONS][0].replace('.', ',').split(', ')  # 캡션의 정보를 받음
    st.title(title)
    st.divider()

    st.header("주의! AI가 생성한 음악의 소리가 '매우' 클 수 있습니다!")
    space(lines=2)

    st.write("### 📃 \t문서 요약 결과 (Summarization)")
    captions = st.multiselect(
        label='',
        options=caption,
        default=caption,
        disabled=True
    )
    space(lines=3)

    # print contents
    music_contents = [MusicContent(caption, audio)
                      for audio in inputs[TAG.AUDIOS]]

    for content in music_contents:
        content.set_content()

    _, button_cols = st.columns([14, 2])
    if button_cols.button("Return"):
        st.session_state[TAG.TEXT_STATE] = 'execute'
        st.experimental_rerun()


# main
if __name__ == "__main__":
    category = get_music_category()          # 각 카테고리의 정보 가져오기

    if TAG.TEXT_STATE not in st.session_state:
        st.session_state[TAG.TEXT_STATE] = 'execute'
    if TAG.TEXT_RES_STATE not in st.session_state:
        st.session_state[TAG.TEXT_RES_STATE] = status.HTTP_200_OK

    # 초기화를 위한 key state생성
    if 'key_num' not in st.session_state:
        st.session_state['key_num'] = TAG.ONE

    delete_another_session_state(TAG.TEXT_STATE)

    if st.session_state[TAG.TEXT_STATE] == 'execute':
        text_analysis(TAG.TEXT_ANALYSIS_TITLE, category=category)

    elif st.session_state[TAG.TEXT_STATE] == 'submit':
        submit_text_analysis(TAG.TEXT_ANALYSIS_TITLE, category=category)

    else:
        result_text_analysis(TAG.MUSIC_OUTPUT_TITLE,
                             st.session_state[TAG.AUDIOFILE])
