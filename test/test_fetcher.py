from downloader.fetcher import FetcherModrinth
import pytest

@pytest.mark.asyncio
async def test_fetch_all():
    fetcher = FetcherModrinth(["https://modrinth.com/mod/sodium"])
    assert await fetcher.fetch_all() != []

@pytest.mark.asyncio
async def test_fetch_all_2():
    fetcher = FetcherModrinth(["https://modrinth.com/mod/sodium", "https://modrinth.com/mod/iris"])
    assert len(await fetcher.fetch_all()) ==2

@pytest.mark.asyncio
async def test_get_latest_version():
    params = {
        'loaders' : ['neoforge'],
        'game_versions': ['1.21.1']
    }
    fetcher = FetcherModrinth(["https://modrinth.com/mod/sodium"], params)
    responses = await fetcher.fetch_all()
    response=await fetcher.get_latest_version(responses)
    assert response[0]["files"][0]["url"] == "https://cdn.modrinth.com/data/AANobbMI/versions/I9RMZOOH/sodium-neoforge-0.6.9%2Bmc1.21.1.jar"

@pytest.mark.asyncio
async def test_get_latest_versions():
    params = {
        'loaders' : ['neoforge'],
        'game_versions': ['1.21.1']
    }
    fetcher = FetcherModrinth(["https://modrinth.com/mod/sodium", "https://modrinth.com/mod/iris"], params)
    responses = await fetcher.fetch_all()
    response=await fetcher.get_latest_version(responses)
    assert response[0]["files"][0]["url"] == "https://cdn.modrinth.com/data/AANobbMI/versions/I9RMZOOH/sodium-neoforge-0.6.9%2Bmc1.21.1.jar" and response[1]["files"][0]["url"] == "https://cdn.modrinth.com/data/YL57xq9U/versions/oXIoDcGE/iris-neoforge-1.8.8%2Bmc1.21.1.jar"

@pytest.mark.asyncio
async def test_download_versions():
    params = {
        'loaders' : ['neoforge'],
        'game_versions': ['1.21.1']
    }
    fetcher = FetcherModrinth(["https://modrinth.com/mod/sodium", "https://modrinth.com/mod/iris"], params)
    responses = await fetcher.fetch_all()
    
    response = await fetcher.get_latest_version(responses)
    assert await fetcher.download_verisons(response) != False

