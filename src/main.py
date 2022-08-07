import asyncio
from distutils.command.upload import upload
from typing import List, Optional
from fastapi import FastAPI
from starlette.responses import Response

from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import cv2
import psycopg2
import json
from pydantic import BaseModel
from pathlib import Path

engine = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user="postgres",
    password=os.getenv("POSTGRES_PASS"),
    host=os.getenv("DB_HOST"),
    port="5432",
)

# John Cena login
get_cena = (
    "select userid from login where username = 'JohnCena' and password = 'badpass';"
)
cursor = engine.cursor()
cursor.execute(get_cena)
uuid = cursor.fetchone()


app = FastAPI()


@app.get("/gpt-3/")
def test_sad(text: str = "") -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {os.environ["OPENAPI_KEY"]}',
    }
    print(text)
    data = (
        r'{"model": "text-davinci-002", "prompt": "Sentence: '
        + text[1:-1]
        + r'\nSuicidality from 0 - 100:", "temperature": 0, "max_tokens": 120}'
    )
    print(data)
    r = requests.post(
        "https://api.openai.com/v1/completions", headers=headers, data=data
    )
    pretty = json.loads(r.text)
    print(pretty["choices"][0]["text"].strip())
    return pretty["choices"][0]["text"].strip().split()[0]


@app.get("/images/{uuid}/{img_id}")
async def get_image(uuid, img_id):
    img = cv2.imread(str(Path("./images", uuid, img_id)))
    res, enc_img = cv2.imencode(".jpg", img)
    return Response(enc_img.tobytes(), media_type="image/jpg")


origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
