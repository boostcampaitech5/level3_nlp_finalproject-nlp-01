import streamlit as st
from streamlit_tags import st_tags
from streamlit_space import space
import requests
from fastapi import status

# custom
from utils.attribute import get_music_category
from utils.config import add_logo, delete_another_session_state, set_page
from utils.log import print_error
from utils.generator import make_category_request_json, make_audio_data
from streamlit_space import space
from models.Content import MusicContent
from constraints import INFO, PATH, TAG, SECRET, COMPONENT

# 카테고리 선택 방식 Page
st.session_state[TAG.BUTTON_NUM] = 0
set_page()
add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)


# 카테고리 선택 페이지
def choice_category(title, category):
    # default 설정 -> 카테고리의 디폴트값 설정
    if TAG.EXTRA_INPUTS not in st.session_state:
        default = COMPONENT.DEFAULT_CATEGORY
    else:
        # 결과페이지에서 돌아온 경우, default값은 선택한 카테고리를 보존
        # duration이 int로 돌아오기 때문에 inb -> index로 변환하는 작업
        duration = st.session_state[TAG.EXTRA_INPUTS][TAG.DURATION]
        duration = str(int(duration/60))+':'+str(duration % 60)
        if len(duration) == 3:
            duration += '0'  # 3:0 인경우가 있음
        for i, s in enumerate(category[TAG.DURATION]):
            if s == duration:
                duration = i
                break
            
        # [] 인 경우, Auto
        if st.session_state[TAG.EXTRA_INPUTS][TAG.TEMPO] == []:
                st.session_state[TAG.EXTRA_INPUTS][TAG.TEMPO] = 'Auto'

        for i, s in enumerate(category[TAG.TEMPO]):
            if s == st.session_state[TAG.EXTRA_INPUTS][TAG.TEMPO]:
                tempo = i
                break

        default = {
            TAG.GENRES: st.session_state[TAG.EXTRA_INPUTS][TAG.GENRES],
            TAG.INSTRUMENTS: st.session_state[TAG.EXTRA_INPUTS][TAG.INSTRUMENTS],
            TAG.MOODS: st.session_state[TAG.EXTRA_INPUTS][TAG.MOODS],
            TAG.ETC: st.session_state[TAG.EXTRA_INPUTS][TAG.ETC],
            TAG.DURATION: duration,  # index이므로
            TAG.TEMPO: tempo,  # index이므로
        }

    # 오류 발생
    if st.session_state[TAG.EXTRA_RES_STATE] != status.HTTP_200_OK:
        st.toast(print_error(st.session_state[TAG.EXTRA_RES_STATE]))
    
    st.title(title)
    st.divider()

    with st.expander(TAG.GUIDE_HEADER):
        st.markdown(INFO.EXTRA_CATEGORY_GUIDE)

    # multiselect
    st.subheader(TAG.GENRES_HEADER)
    genres = st.multiselect(
        label=TAG.GENRES_DESCRIPTION,
        options=category[TAG.GENRES],
        default=default[TAG.GENRES],
        key="genres"+st.session_state['key_num'])
    space(lines=1)

    st.subheader(TAG.MOODS_HEADER)
    moods = st.multiselect(
        label=TAG.MOODS_DESCRIPTION,
        options=category[TAG.MOODS],
        default=default[TAG.MOODS],
        key="moods"+st.session_state['key_num'])
    space(lines=1)

    st.subheader(TAG.INSTRUMENTS_HEADER)
    instruments = st.multiselect(
        label=TAG.INSTRUMENTS_DESCRIPTION,
        options=category[TAG.INSTRUMENTS],
        default=default[TAG.INSTRUMENTS],
        key="instruments"+st.session_state['key_num'])
    space(lines=1)

    # 사용자 keywords 생성
    etc = st_tags(
        label=TAG.ETC_HEADER,
        text=TAG.ETC_DESCRIPTION,
        suggestions=category[TAG.ETC],
        value=default[TAG.ETC],
        key="etc"+st.session_state['key_num'])
    space(lines=1)

    col_1, col_2 = st.columns([1, 1], gap="large")

    col_1.subheader(TAG.DURATION_HEADER)
    duration = col_1.selectbox(
        label=TAG.DURATION_DESCRIPTION,
        options=category[TAG.DURATION],
        index=default[TAG.DURATION],
        key="duration"+st.session_state['key_num'])

    col_2.subheader(TAG.TEMPO_HEADER)
    tempo = col_2.radio(
        label=TAG.TEMPO_DESCRIPTION,
        options=category[TAG.TEMPO],
        index=default[TAG.TEMPO],
        key="tempo"+st.session_state['key_num'])

    button_cols_1, button_cols_2 = st.columns([14, 2])
    if button_cols_1.button('초기화'):  # 결과페이지에서 Return을 누르고 돌아오면 작동하지만, 첫화면에서는 작동 안됨
        if TAG.EXTRA_INPUTS in st.session_state:
            del st.session_state[TAG.EXTRA_INPUTS]

        # key값 변경
        if st.session_state['key_num'] == TAG.ONE:
            st.session_state['key_num'] = TAG.TWO
        else:
            st.session_state['key_num'] = TAG.ONE

        st.experimental_rerun()

    if button_cols_2.button("Submit"):  # 제출버튼

        # duration 파싱 -> str to int로 바꿔서 API서버로 전송
        min, sec = map(int, duration.split(':'))
        duration = min*60 + sec

        # API로 전송하기 위해 input생성
        inputs = {
            TAG.GENRES: genres,
            TAG.INSTRUMENTS: instruments,
            TAG.MOODS: moods,
            TAG.ETC: etc,
            TAG.DURATION: duration,
            TAG.TEMPO: tempo,
        }

        # 입력이 없다면
        if inputs[TAG.GENRES] == [] and inputs[TAG.INSTRUMENTS] == [] and inputs[TAG.MOODS] == [] and inputs[TAG.ETC] == []:
            st.toast('입력을 확인해 주세요!')

        else:
            # tempo가 Auto인 경우
            if inputs[TAG.TEMPO] == 'Auto':
                inputs[TAG.TEMPO] = []

            # 선택한 카테고리를 세션으로 저장해둠 -> 다시 Return으로 돌아갈 경우 default로 사용
            st.session_state[TAG.EXTRA_INPUTS] = inputs

            # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
            st.session_state[TAG.EXTRA_STATE] = 'submit'
            st.experimental_rerun()


# 제출페이지 누르면 실행 -> disabled=True, button 삭제, post요청 보내고 spinner가 돌아감
def submit_choice_category(title, category):

    # default 설정 -> 카테고리의 디폴트값 설정
    if TAG.EXTRA_INPUTS not in st.session_state:
        default = COMPONENT.DEFAULT_CATEGORY
    else:
        # 결과페이지에서 돌아온 경우, default값은 선택한 카테고리를 보존
        # duration이 int로 돌아오기 때문에 inb -> index로 변환하는 작업
        duration = st.session_state[TAG.EXTRA_INPUTS][TAG.DURATION]
        duration = str(int(duration/60))+':'+str(duration % 60)
        if len(duration) == 3:
            duration += '0'  # 3:0 인경우가 있음
        for i, s in enumerate(category[TAG.DURATION]):
            if s == duration:
                duration = i
                break
        
        # [] 인 경우, Auto
        if st.session_state[TAG.EXTRA_INPUTS][TAG.TEMPO] == []:
                st.session_state[TAG.EXTRA_INPUTS][TAG.TEMPO] = 'Auto'

        for i, s in enumerate(category[TAG.TEMPO]):
            if s == st.session_state[TAG.EXTRA_INPUTS][TAG.TEMPO]:
                tempo = i
                break

        default = {
            TAG.GENRES: st.session_state[TAG.EXTRA_INPUTS][TAG.GENRES],
            TAG.INSTRUMENTS: st.session_state[TAG.EXTRA_INPUTS][TAG.INSTRUMENTS],
            TAG.MOODS: st.session_state[TAG.EXTRA_INPUTS][TAG.MOODS],
            TAG.ETC: st.session_state[TAG.EXTRA_INPUTS][TAG.ETC],
            TAG.DURATION: duration,  # index이므로
            TAG.TEMPO: tempo,  # index이므로
        }

    # 오류 발생
    if st.session_state[TAG.EXTRA_RES_STATE] != status.HTTP_200_OK:
        st.toast(st.session_state[TAG.EXTRA_RES_STATE])

    st.title(title)
    st.write("---")

    with st.expander(TAG.GUIDE_HEADER):
        st.markdown(INFO.EXTRA_CATEGORY_GUIDE)

    # multiselect
    st.subheader(TAG.GENRES_HEADER)
    genres = st.multiselect(
        label=TAG.GENRES_DESCRIPTION,
        options=category[TAG.GENRES],
        default=default[TAG.GENRES],
        disabled=True)
    space(lines=1)

    st.subheader(TAG.MOODS_HEADER)
    moods = st.multiselect(
        label=TAG.MOODS_DESCRIPTION,
        options=category[TAG.MOODS],
        default=default[TAG.MOODS],
        disabled=True)
    space(lines=1)

    st.subheader(TAG.INSTRUMENTS_HEADER)
    instruments = st.multiselect(
        label=TAG.INSTRUMENTS_DESCRIPTION,
        options=category[TAG.INSTRUMENTS],
        default=default[TAG.INSTRUMENTS],
        key="instruments"+st.session_state['key_num'])
    space(lines=1)

    # 사용자 keywords 생성
    st.subheader(TAG.ETC_HEADER[3:])
    etc = st.multiselect(
        label=TAG.ETC_DESCRIPTION,
        options=default[TAG.ETC],
        default=default[TAG.ETC],
        disabled=True)
    space(lines=1)

    col_1, col_2 = st.columns([1, 1], gap="large")

    col_1.subheader(TAG.DURATION_HEADER)
    duration = col_1.selectbox(
        label=TAG.DURATION_DESCRIPTION,
        options=category[TAG.DURATION],
        index=default[TAG.DURATION],
        disabled=True)

    col_2.subheader(TAG.TEMPO_HEADER)
    tempo = col_2.radio(
        label=TAG.TEMPO_DESCRIPTION,
        options=category[TAG.TEMPO],
        index=default[TAG.TEMPO],
        disabled=True)

    with st.spinner(TAG.REQUEST_MESSAGE):
        my_json = make_category_request_json(
            st.session_state[TAG.EXTRA_INPUTS])
        res = requests.post(SECRET.MUSICGEN_CATEGORY_URL, json=my_json)
        print(res)      # log로 요청이 제대로 왔는지 확인

        st.session_state[TAG.EXTRA_RES_STATE] = res.status_code

        if res.status_code != status.HTTP_200_OK:
            st.session_state[TAG.EXTRA_STATE] = 'execute'
            st.experimental_rerun()
        else:
            audio_files, caption = make_audio_data(res)
            st.session_state[TAG.AUDIOFILE] = {
                TAG.AUDIOS: audio_files, TAG.CAPTIONS: caption}

            st.session_state['res'] = res
            st.session_state[TAG.EXTRA_STATE] = 'result'
            st.experimental_rerun()


# 결과 페이지
def result_choice_category(title, inputs):
    caption = [cpt for cpt in inputs[TAG.CAPTIONS]
               [0].split(', ') if cpt]  # 캡션의 정보를 받음
    st.title(title)
    st.divider()

    st.write("### 📃 \t캡션 정보 (Caption)")
    captions = st.multiselect(
        label='',
        options=caption,
        default=caption,
        disabled=True
    )
    space(lines=3)

    # 음악, 다운로드 버튼 생성
    music_contents = [MusicContent(caption, w) for w in inputs[TAG.AUDIOS]]
    for content in music_contents:
        content.set_content()

    _, button_cols = st.columns([14, 2])

    # 카테고리 선택화면으로 돌아가기
    if button_cols.button("Return"):
        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        st.session_state[TAG.EXTRA_STATE] = 'execute'
        st.experimental_rerun()


# main
if __name__ == "__main__":
    category = get_music_category()

    # state가 없으면 생성
    if TAG.EXTRA_STATE not in st.session_state:
        st.session_state[TAG.EXTRA_STATE] = 'execute'
    if TAG.EXTRA_RES_STATE not in st.session_state:
        st.session_state[TAG.EXTRA_RES_STATE] = status.HTTP_200_OK

    # key값을 변경 -> 값의 초기화하고 새로고침을 만들기 위해 key값을 다르게 설정
    if 'key_num' not in st.session_state:
        st.session_state['key_num'] = TAG.ONE
    

    # 다른 state 제거
    delete_another_session_state(TAG.EXTRA_STATE)

    # state가 execute인 경우, 카테고리 선택페이지를 출력
    if st.session_state[TAG.EXTRA_STATE] == 'execute':
        choice_category(title=TAG.EXTRA_CATEGORY_TITLE, category=category)

    elif st.session_state[TAG.EXTRA_STATE] == 'submit':
        submit_choice_category(
            title=TAG.EXTRA_CATEGORY_TITLE, category=category)

    # state가 result인 경우 결과화면을 출력
    else:
        result_choice_category(TAG.MUSIC_OUTPUT_TITLE,
                               st.session_state[TAG.AUDIOFILE])
