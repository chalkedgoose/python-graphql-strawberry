import asyncio
import strawberry
from typing import AsyncIterable, List
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


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
            title='The Great Gatsby',
            author='F. Scott Fitzgerald',
        ),
        Book(
            title='Das Kapital',
            author='Karl Marx'
        ),
        Book(
            title='Animal Farm',
            author='George Orwell'
        )
    ]


@strawberry.type
class Query:
    @strawberry.field
    def books(self, title: str) -> List[Book]:

        if title:
            return [book for book in get_books() if book.title == title]

        return get_books()

    @strawberry.field
    def user(self) -> User:
        x = self
        v = "Carlos"
        return User("Carlos", age=22)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        return Book(title=title, author=author)


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

app.include_router(graphql_app, prefix="/graphql")
