from downloader.fetcher import FetcherModrinth
import pytest

@pytest.mark.asyncio
async def test_fetch_all():
    fetcher = FetcherModrinth(["https://modrinth.com/mod/sodium"])
    assert await fetcher.fetch_all() != []

@pytest.mark.asyncio
async def test_get_latest_version():
    params = {
        'loaders' : ['neoforge'],
        'game_versions': ['1.21.1']
    }
    fetcher = FetcherModrinth(["https://modrinth.com/mod/sodium"], params)
    responses = await fetcher.fetch_all()
    assert await fetcher.get_latest_version(responses) != None