from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel

class CategoryInput(BaseModel):
    genre: List[str]
    instrument: List[str]
    mood: List[str]
    etc: List[str]

class TextInput(BaseModel):
    genre: List[str]
    instrument: List[str]
    mood: List[str]
    etc: List[str]
    text: str

app = FastAPI()
    

@app.get("/")
def test():
    print("hello~")


@app.post("/choice_category")
def choice_category(inputs: CategoryInput):
    print(inputs)


@app.post("/text_analysis")
def text_analysis(inputs: TextInput):
    print(inputs)