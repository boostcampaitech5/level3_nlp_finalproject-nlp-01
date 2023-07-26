import streamlit as st
from PIL import Image
from streamlit_space import space

from constraints import PATH, TAG


class MusicContent():
    def __init__(self, caption, file):
        self.caption = caption
        self.music_file = file

    def set_content(self):
        button_num = st.session_state[TAG.BUTTON_NUM]

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
            st.audio(self.music_file,
                     format=TAG.AUDIO_TYPE)
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
        st.session_state[TAG.BUTTON_NUM] += 1


class Demo():
    def __init__(self, caption, music_path_list):
        self.caption = caption
        self.music = []

        for path in music_path_list:
            self.music.append(open(path, 'rb').read())

    def set_content(self):
        length = len(self.music)
        cols = st.columns([4]+[5]*length)

        with cols[0]:
            st.write(f"##### {self.caption}")
        for idx, col in enumerate(cols[1:]):
            with col:
                st.audio(self.music[idx], format=TAG.AUDIO_TYPE)
        space(lines=3)
