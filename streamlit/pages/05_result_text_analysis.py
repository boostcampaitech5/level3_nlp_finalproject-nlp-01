MUSIC_PATH = "./streamlit/assets/test_music.wav"

TEST_CAPTION = ["Orchestral", "With a strings", "Cinematic", "Slow bpm"]
button_num = 0
class TextAnalysisContent():
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
        </style>
        """, unsafe_allow_html=True)

        # 첫번째 라인
        self.col00, self.col01 = st.columns([1, 10])
        with self.col00:        # 아이콘 부분
            icon = Image.open(IMAGE_ICON_PATH)
            st.image(icon)
        with self.col01:        # 캡션 부분
            caption = ', '.join(self.caption)
            st.markdown(
                f'<p class="big-font">{caption}</p>', unsafe_allow_html=True)

        # 두번째 라인
        self.col10, self.col11 = st.columns([10, 2])
        with self.col10:        # 음악 재생 부분
            st.audio(self.music_file, format='audio/ogg')
        with self.col11:        # 다운로드 부분
            music_caption = '_'.join(self.caption)
            st.download_button(
                label=":blue[DOWNLOAD]",        # 버튼 라벨 텍스트
                key=f"button{str(button_num)}",
                data=self.music_file,
                file_name=f"{music_caption}_music.wav"
            )
            button_num += 1     # 버튼은 key값을 지정해야 하기때문에 임의로 Key를 지정
        space(lines=2)      # 컨텐츠 구분을 짓기 위한 개행 처리
    summary_text = "Orchestral, with a strings, cinematic, slow bpm"
    audio_file = open(MUSIC_PATH, 'rb').read()
