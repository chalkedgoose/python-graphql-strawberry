import asyncio
from distutils.command.upload import upload
import strawberry
from strawberry.file_uploads import Upload
from typing import List, Optional
from fastapi import FastAPI
from starlette.responses import StreamingResponse, Response

from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import cv2
import psycopg2

# connect to database
engine = psycopg2.connect(
    database="depression-solved",
    user="backend",
    password="goodpass",
    host="depression-solved.cro2y7qspvtf.us-east-2.rds.amazonaws.com",
    port="5432",
)


@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Book:
    title: str
    author: str


def get_books():
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
        Book(title="Das Kapital", author="Karl Marx"),
        Book(title="Animal Farm", author="George Orwell"),
    ]


@strawberry.type
class Query:
    @strawberry.field
    def books(self, title: Optional[str] = None) -> List[Book]:

        if title is not None:
            return [book for book in get_books() if book.title == title]

        return get_books()

    @strawberry.field
    def user(self) -> User:
        x = self
        v = "Carlos"
        return User("Carlos", age=22)

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
    img = cv2.imread(img_id)
    res, enc_img = cv2.imencode(".jpg", img)
    return Response(enc_img.tobytes(), media_type="image/jpg")


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

graphql_app = GraphQLRouter(schema)


origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")
