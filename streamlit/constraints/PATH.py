import os

BASE_PATH = "streamlit" if os.getcwd().split('\\')[-1] != "streamlit" else ""
DEMO = os.path.join(BASE_PATH, "demo")

SIDEBAR_IMAGE_PATH = os.path.join(
    BASE_PATH, "assets", "sidebar_img.png")
DATA_PATH = os.path.join(BASE_PATH, "assets", "category_ver1.0.3.json")
IMAGE_ICON_PATH = os.path.join(BASE_PATH, "assets", "music_icon.png")
ICON_PATH = os.path.join(BASE_PATH, "assets", 'page_icon.png')
MAIN_IMAGE = os.path.join(BASE_PATH, "assets", 'main_image.png')
SECRET_FILE = os.path.join(BASE_PATH, "assets", "secret.json")


# 테스트용
TEST_MUSIC_PATH = os.path.join(BASE_PATH, "assets", "test_music.wav")
TEST_CAPTION = ["Orchestral", "With a strings", "Cinematic", "Slow bpm"]
