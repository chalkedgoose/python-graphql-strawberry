
import pytest
from src.main import schema


@pytest.mark.asyncio
async def test_books_query():
    query = """
        query TestBooksQuery {
            books {
                title
                author
            }
        }
    """

    result = await schema.execute(
        query
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["books"] == [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
        },
        {
            "title": "Das Kapital",
            "author": "Karl Marx"
        },
        {
            "title": "Animal Farm",
            "author": "George Orwell"
        }
    ]


@pytest.mark.asyncio
async def test_books_query_with_arguments():
    query = """
        query TestBooksQueryWithArguments($title: String!) {
            books(title: $title) {
                title
                author
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={"title": "The Great Gatsby"},
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["books"] == [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
        }
    ]
