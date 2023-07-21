import urllib.request
import urllib
from googletrans import Translator  # googletrans==3.1.0a0

import openai


def google_trans(text):
    translator = Translator()
    result = translator.translate(text, src='ko', dest='en')
    return result.text


def create_gpt_caption(res):
    genre, summary = res['genre'], res['summary']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Based on the contents of {genre} as genre and {summary} as story, please create a caption that expresses musical elements such as genre, instrument, emotion, and song style.\
             Just like the following sentence: Meditative song, calming and soothing, with flutes and guitars. The music is slow, with a focus on creating a sense of peace and tranquility."},
            {"role": "assistant", "content": "Meditative song, calming and soothing, with flutes and guitars. The music is slow, with a focus on creating a sense of peace and tranquility."},
        ]
    )

    return response['choices'][0]['message']['content']
