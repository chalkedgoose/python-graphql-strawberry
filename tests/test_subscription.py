import pytest
from src.main import schema


@pytest.mark.asyncio
async def test_subscription():
    query = """
        subscription {
            count(target: 3)
        }
    """

    sub = await schema.subscribe(query)

    index = 0
    async for result in sub:  # type: ignore
        assert not result.errors
        assert result.data == {"count": index}

        index += 1
