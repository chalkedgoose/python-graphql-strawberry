from typing import List
from src.models.Book import Book

# Repository for interacting with user data.


class BookRepo:
    books_db = [
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

    def get_books(self) -> List[Book]:
        return self.books_db

    def get_book_by_title(self, title: str) -> List[Book]:
        return [book for book in self.get_books() if book.title == title]

    def create_book(self, title: str, author: str) -> Book:
        new_book = Book(title, author)
        self.books_db.append(new_book)
        return new_book
