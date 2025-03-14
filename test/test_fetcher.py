from downloader.fetcher import FetcherModrinth
import pytest

@pytest.mark.asyncio
async def test_all():
    fetcher = FetcherModrinth(["https://modrinth.com/mod/eureka"], "")
    assert await fetcher.fetch_all() != []
