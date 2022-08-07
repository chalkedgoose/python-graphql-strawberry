import asyncio

from distutils.command.upload import upload
import strawberry
from strawberry.file_uploads import Upload
from typing import List, Optional

from dataclasses import asdict
from distutils.command.upload import upload
import strawberry
from strawberry.file_uploads import Upload
from typing import Dict, List, Optional

from fastapi import FastAPI
from starlette.responses import StreamingResponse, Response

from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import cv2
import psycopg2
import boto3
import botocore


engine = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user="postgres",
    password=os.getenv("POSTGRES_PASS"),
    host=os.getenv("DB_HOST"),
    port="5432",
)


s3 = boto3.resource("s3")
bucket = s3.Bucket("memoimages")
exists = True
try:
    s3.meta.client.head_bucket(Bucket="memoimages")
except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = e.response["Error"]["Code"]
    if error_code == "404":
        exists = False

import requests
import os
import cv2
import psycopg2
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

@strawberry.type
class Query:
    @strawberry.field
    def test_sad(self, text: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {os.environ["OPENAPI_KEY"]}',
        }
        data = (
            r'{"model": "text-davinci-002", "prompt": "Sentence: \"'
            + text
            + r'\"\n% probability of extreme sadness:", "temperature": 0, "max_tokens": 120}'
        )
        r = requests.post(
            "https://api.openai.com/v1/completions", headers=headers, data=data
        )
        return r.text


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> str:
        return Book(title=title, author=author)


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> int:  # type: ignore
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)

app = FastAPI()


@app.get("/images/{uuid}/{img_id}")
async def get_image(uuid, img_id):
    """
    uuid is either "mechanims", "values", or unique user ID.
    img_id the image number from the database. i.e from mech-id, values-id, image id in the user id folder
    """
    img = cv2.imread(img_id)
    res, enc_img = cv2.imencode(".jpg", img)

    return Response(enc_img.tobytes(), media_type="image/jpg")


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

@app.get("/images/{uuid}/{img_id}")
async def get_image(uuid, img_id):
    img = cv2.imread(img_id)
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


@app.get("/submissions")
def read_submissions():
    return [asdict(x) for x in SubmissionRepo().get_submissions()]
