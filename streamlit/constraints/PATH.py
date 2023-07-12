import os

BASE_PATH = "streamlit" if os.getcwd().split('\\')[-1] != "streamlit" else ""
SIDEBAR_IMAGE_PATH = os.path.join(BASE_PATH, "assets", "sidebar_logo.png")
DATA_PATH = os.path.join(BASE_PATH, "assets", "category_ver1.0.0.json")
IMAGE_ICON_PATH = os.path.join(BASE_PATH, "assets", "music_icon.png")
