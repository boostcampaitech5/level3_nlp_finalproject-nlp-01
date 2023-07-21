# -*- coding: utf-8 -*-
import os

# streamlit tools
import streamlit as st
from streamlit_space import space
from PIL import Image

# custom
from utils import add_logo, delete_another_session_state
from constraints import PATH, INFO


st.set_page_config(
    page_title=INFO.PROJECT_NAME,
    page_icon=PATH.ICON_PATH,
    layout="wide"
)


class DemoContent():
    def __init__(self, caption, music_path_list):
        self.caption = caption
        self.music = []

        for path in music_path_list:
            self.music.append(open(path, 'rb').read())

    def set_content(self):
        length = len(self.music)
        cols = st.columns([4]+[5]*length)

        with cols[0]:
            st.write(self.caption)
        for idx, col in enumerate(cols[1:]):
            with col:
                st.audio(self.music[idx], format='audio/wav')
        space(lines=3)


def guide():
    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)

    delete_another_session_state(' ')

    st.title(INFO.PROJECT_NAME)
    st.divider()

    main_col0, main_col1 = st.columns([2, 6], gap="large")
    with main_col0:
        icon = Image.open(PATH.MAIN_IMAGE).resize((400, 400))
        st.image(icon)
    with main_col1:
        st.markdown(INFO.PROJECT_DETAIL)

    space(lines=3)

    st.markdown("# 데모 버젼")
    st.divider()

    # 데모 불러오기
    demos = os.listdir(PATH.DEMO)
    for demo in demos:
        music_paths = [os.path.join(PATH.DEMO, demo, file)
                       for file in os.listdir(os.path.join(PATH.DEMO, demo))]
        DemoContent(demo, music_paths).set_content()


guide()
