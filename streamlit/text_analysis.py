import json
import requests
import streamlit as st

# streamlit tools
from streamlit_tags import st_tags
from streamlit_space import space


# 문서 분석 방식


def text_analysis(title):

    st.title(title)
    st.write("---")

    space(lines=2)

    space(lines=2)
    # text area
    space(lines=1)
