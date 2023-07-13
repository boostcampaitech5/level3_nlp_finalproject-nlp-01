import os
import numpy as np
import streamlit as st
from streamlit_tags import st_tags
from streamlit_space import space
from PIL import Image


# custom
from utils import add_logo, delete_another_session_state, get_music_category
from streamlit_space import space
from constraints import PATH, TAG

# 카테고리 선택 방식 Page
button_num = 0
TEST_MUSIC_PATH = os.path.join(PATH.BASE_PATH, "assets", "test_music.wav")
TEST_CAPTION = ["Orchestral", "With a strings", "Cinematic", "Slow bpm"]

class CategoryChoiceContent():
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
        button {
            height: auto;
            padding-top: 14px !important;
            padding-bottom: 14px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # 첫번째 라인
        col_0, col_1, col_2 = st.columns([2, 13, 3])
        with col_0:     # 아이콘 부분
            icon = Image.open(PATH.IMAGE_ICON_PATH).resize((60, 60))
            st.image(icon)
        with col_1:     # 음악 재생 부분
            st.audio(self.music_file, format='audio/ogg')
        with col_2:
            music_caption = '_'.join(self.caption)
            st.download_button(
                label=":blue[DOWNLOAD]",    # 버튼 라벨 텍스트
                key=f"button{str(button_num)}",
                data=self.music_file,
                file_name=f"{music_caption}_music.wav"
            )
            button_num += 1     # 버튼은 key값을 지정해야 하기때문에 임의로 Key를 지정
        space(lines=1)      # 컨텐츠 구분을 짓기 위한 개행 처리


# 카테고리 선택 페이지
def choice_category(title, options):

    # default 설정
    if "choice_inputs" not in st.session_state:
        default = {
            "genre": [],
            "instruments": [],
            "mood": [],
            "etc": [],
            "duration": 1, # index이므로
            "tempo": 1, # index이므로
        }
    else:
        duration = st.session_state['choice_inputs']['duration']
        duration = str(int(duration/60))+':'+str(duration%60)
        for i, s in enumerate(options['duration']):
            if s == duration:
                duration = i
                break
        
        for i, s in enumerate(options['tempo']):
            if s == st.session_state['choice_inputs']['tempo']:
                tempo = i
                break
        
        default = {
            "genre": st.session_state['choice_inputs']['genre'],
            "instruments": st.session_state['choice_inputs']['instruments'],
            "mood": st.session_state['choice_inputs']['mood'],
            "etc": st.session_state['choice_inputs']['etc'],
            "duration": duration, # index이므로
            "tempo": tempo, # index이므로
        }

    st.title(title)
    st.write("---")

    with st.expander("설명"):
        st.write("사용법 설명")

    # multiselect
    st.subheader('🎼 장르 (Genre)')
    genre = st.multiselect(
        label='생성할 음악의 장르를 선택해 주세요.',
        options=options[TAG.GENRES],
        default=default['genre'])
    space(lines=1)

    st.subheader('🥁 악기 (Musical Instruments)')
    instruments = st.multiselect(
        label='생성할 음악의 악기를 선택해 주세요.',
        options=options[TAG.INSTRUMENTS],
        default=default['instruments'])
    space(lines=1)

    st.subheader('📣 분위기 (Mood)')
    mood = st.multiselect(
        label='생성할 음악의 분위기를 선택해 주세요.',
        options=options[TAG.MOODS],
        default=default['mood'])
    space(lines=1)

    # 사용자 keywords 생성
    etc = st_tags(
        label='### ⚙ 기타 (ETC)',
        text='생성할 음악의 추가정보를 입력해 주세요',
        value=default['etc'],
        suggestions=[])
    space(lines=1)

    col_1, col_2 = st.columns([1, 1], gap="large")

    col_1.subheader('⌛ 길이(Duration)')
    duration = col_1.selectbox(
        label='생성할 음악의 길이를 선택해 주세요',
        options=options['duration'],
        index=default['duration'])

    col_2.subheader('🏇 속도 (Tempo)')
    tempo = col_2.radio(
        label='생성할 음악의 빠르기를 선택해 주세요', 
        options=options['tempo'], 
        index=default['tempo'])

    button_cols_1, button_cols_2 = st.columns([14, 2])
    if button_cols_1.button('초기화'):
        if "choice_inputs" in st.session_state:
            del st.session_state['choice_inputs']
            st.experimental_rerun()

    if button_cols_2.button("Submit"):

        # duration 파싱
        min, sec = map(int, duration.split(':'))
        duration = min*60 + sec

        # input 생성
        inputs = {
            "genre": genre,
            "instruments": instruments,
            "mood": mood,
            "etc": etc,
            "duration": duration,
            "tempo": tempo,
        }
        
        st.session_state['choice_inputs'] = inputs

        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        # res = requests.post(url = "http://127.0.0.1:8000/choice_category", data = json.dumps(inputs))

        # session_state 변경 -> result 페이지로 이동
        st.session_state['choice_state'] = 'result'
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
    caption = inputs['captions']
    st.title(title)
    st.write("---")

    st.write("### 📃 \t캡션 정보 (Caption)")
    captions = st.multiselect(
        label='',
        options=inputs['captions'],
        default=inputs['captions'],
        disabled=True
    )
    space(lines=3)

    music_contents = [CategoryChoiceContent(caption, w) for w in inputs['wav']]
    for content in music_contents:
        content.set_content()

    _, button_cols = st.columns([14, 2])

    if button_cols.button("Return"):
        # TO DO : 리스트를 모델 서버로 전달 -> 다시 생성된 음악 파일 받고 올림
        st.session_state['choice_state'] = 'execute'
        st.experimental_rerun()


# main


if __name__ == "__main__":

    
    # 임시 options -> DB에서 받을 예정
    options = get_music_category()
    options['tempo'] = ['Slow', 'Medium', 'Fast']
    options['duration'] = ['0:10', '0:30', '1:00', '1:30', '2:00', '3:00']

    audio_file = open(TEST_MUSIC_PATH, 'rb').read()

    if 'choice_state' not in st.session_state:
        st.session_state['choice_state'] = 'execute'

    delete_another_session_state('choice_state')

    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)

    if st.session_state['choice_state'] == 'execute':
        choice_category(title='카테고리 선택', options=options)

    else:
        # 임시 input 생성
        inputs = {
            'captions': TEST_CAPTION,
            'wav': [audio_file, audio_file, audio_file, audio_file]
        }

        result_choice_category('🎧 Music Generate Result', inputs)
