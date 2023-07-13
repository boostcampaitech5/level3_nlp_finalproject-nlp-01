# -*- coding: utf-8 -*-
import os

# streamlit tools
import streamlit as st
from streamlit_space import space
from PIL import Image

# custom
from utils import add_logo
from constraints import PATH, INFO


st.set_page_config(
    page_title=INFO.PROJECT_NAME,
    page_icon=PATH.ICON_PATH,
)


class DemoContent():
    def __init__(self, caption, music_path_list):
        self.caption = caption
        self.music = []

        for path in music_path_list:
            self.music.append(open(path, 'rb').read())

    def set_content(self):
        length = len(self.music)
        cols = st.columns([4]+[3]*length)

        with cols[0]:
            st.write(self.caption)
        for idx, col in enumerate(cols[1:]):
            with col:
                st.audio(self.music[idx], format='audio/ogg')
        space(lines=3)


def guide():
    add_logo(PATH.SIDEBAR_IMAGE_PATH, height=250)

    st.title("TextTuneS")
    st.write("---")

    main_col0, main_col1 = st.columns([5, 5], gap="large")
    with main_col0:
        icon = Image.open(PATH.MAIN_IMAGE).resize((1280, 1280))
        st.image(icon)
    with main_col1:
        st.markdown("### 크리에이터를 위한 음악생성 서비스")
        st.write(
            "저희 **Textunes**는 많은 컨텐츠 크리에이터들을 위한 프로젝트 입니다. 누구나 쉽고 간단하게 나만의 커스터마이징한 음악을 만들 수 있습니다.")
        st.write("음악 생성 모델을 통해서 컨텐츠를 더 완성도 높게 만들어 보세요.")

    space(lines=5)

    st.subheader("데모 버젼")
    st.write("---")

    # 데모 불러오기
    demos = os.listdir(PATH.DEMO)
    for demo in demos:
        music_paths = [os.path.join(PATH.DEMO, demo, file)
                       for file in os.listdir(os.path.join(PATH.DEMO, demo))]
        DemoContent(demo, music_paths).set_content()


guide()
