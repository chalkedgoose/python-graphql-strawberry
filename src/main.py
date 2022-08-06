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

from src.repositories.BookRepo import BookRepo
from src.repositories.UserRepo import UserRepo
from src.models.User import User
from src.models.Book import Book

@strawberry.type
class Query:
    @strawberry.field
    def books(self, title: Optional[str] = None) -> List[Book]:
        book_repo = BookRepo()

        if title is not None:
            return book_repo.get_book_by_title(title)

        return book_repo.get_books()

    @strawberry.field
    def users(self) -> List[User]:
        return UserRepo().get_users()

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
    def add_book(self, title: str, author: str) -> Book:
        return BookRepo().create_book(title, author)


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
