import pytest
from src.main import schema


@pytest.mark.asyncio
async def test_add_book_mutation():
    mutation = """
        mutation TestAddBookMutation($title: String!, $author: String!) {
            addBook(title: $title, author: $author) {
                title
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "title": "The Little Prince",
            "author": "Antoine de Saint-Exupéry"
        }
    )

    assert resp.errors is None
    assert resp.data is not None
    assert resp.data["addBook"] == {
        "title": "The Little Prince"
    }
