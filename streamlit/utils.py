import json
from typing import List


def get_component(tag: str) -> List:
    with open("./streamlit/assets/component_data.json", "r") as file:
        component = json.load(file)

    return component[tag]
