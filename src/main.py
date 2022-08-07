import asyncio
from distutils.command.upload import upload
from optparse import Values
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
import random

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

import requests
import os
import cv2
import sys


from src.repositories.BookRepo import BookRepo
from src.repositories.SubmissionsRepo import SubmissionRepo
from src.repositories.UserRepo import UserRepo

from src.models.User import User
from src.models.Book import Book
from src.models.Submission import Submission

sys.path.insert(1, "./src/")
from images import make_folders

make_folders()


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
        + text.replace('"', "")
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
    """
    uuid is either "mechanims", "values", or unique user ID.
    img_id the image number from the database. i.e from mech-id, values-id, image id in the user id folder
    """
    img = cv2.imread(str(Path("./images", uuid, img_id)))
    res, enc_img = cv2.imencode(".jpg", img)
    return Response(enc_img.tobytes(), media_type="image/jpg")


@app.get("/random/{uuid}")
async def get_rand_img(uuid):
    p = Path("./images", uuid)
    images = os.listdir(str(p))
    full = p / random.choice(images)
    img = cv2.imread(str(full))
    res, enc_img = cv2.imencode(".jpg", img)
    return Response(enc_img.tobytes(), media_type="image/jpg")


@app.get("/story/{page}")
async def get_page(page):
    get_values = "select memotext from PHATtable order by date;"
    cursor.execute(get_values)
    texts = cursor.fetchall()
    builder = {
        "mechanisms": ["/random/mechanisms"] * 3,
        "values": ["/random/values"] * 3,
        "bannerImg": "/random/user",
        "journal": texts[int(page) % len(texts)][0],
    }
    return json.dumps(builder)


origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
