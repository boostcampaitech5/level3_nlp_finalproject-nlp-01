from fastapi import FastAPI
import uvicorn
from typing import List, Union
from pydantic import BaseModel
import time

class CategoryInput(BaseModel):
    genres: Union[List[str], None]
    instruments: Union[List[str], None]
    moods: Union[List[str], None]
    etc: Union[List[str], None]
    duration: int
    tempo: str

class TextInput(BaseModel):
    etc: Union[List[str], None]
    text: str
    duration: int
    tempo: str


app = FastAPI()
    

@app.get("/")
def test():
    print("hello~")


@app.post("/choice_category")
def choice_category(inputs: CategoryInput):
    print(inputs)
    time.sleep(5)
    return {"message": "test"}


@app.post("/text_analysis")
def text_analysis(inputs: TextInput):
    print(inputs)
    time.sleep(5)
    return {"message": "test"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    