import os

BASE_PATH = "streamlit" if os.getcwd().split('\\')[-1] != "stramlit" else ""
SIDEBAR_IMAGE_PATH = os.path.join(BASE_PATH, "assets", "sidebar_logo.png")
