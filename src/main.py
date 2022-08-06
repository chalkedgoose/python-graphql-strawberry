import asyncio
import strawberry
from typing import List, Optional
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware
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


schema = strawberry.Schema(
    query=Query, mutation=Mutation, subscription=Subscription)

graphql_app = GraphQLRouter(schema)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")
