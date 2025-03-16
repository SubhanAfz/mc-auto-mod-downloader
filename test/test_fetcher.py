from downloader.fetcher import FetcherModrinth
import pytest

@pytest.mark.asyncio
async def test_fetch_all():
    fetcher = FetcherModrinth(["https://modrinth.com/mod/sodium"])
    assert await fetcher.fetch_all() != []

@pytest.mark.asyncio
async def test_fetch_all_2():
    fetcher = FetcherModrinth(["https://modrinth.com/datapack/terralith"])
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
async def test_get_latest_version_2():
    params = {
        'loaders' : ['neoforge'],
        'game_versions': ['1.21.1']
    }
    fetcher = FetcherModrinth(["https://modrinth.com/datapack/terralith"], params)
    responses = await fetcher.fetch_all()
    response=await fetcher.get_latest_version(responses)
    print(response)
    assert response[0]["files"][0]["url"] == "https://cdn.modrinth.com/data/8oi3bsk5/versions/MuJMtPGQ/Terralith_1.21.x_v2.5.8.jar"

@pytest.mark.asyncio
async def test_get_latest_version_2():
    params = {
        'loaders' : ['neoforge'],
        'game_versions': ['1.21.1']
    }
    fetcher = FetcherModrinth(["https://modrinth.com/plugin/simple-voice-chat"], params)
    responses = await fetcher.fetch_all()
    response=await fetcher.get_latest_version(responses)
    print(response)
    assert response[0]["files"][0]["url"] == "https://cdn.modrinth.com/data/9eGKb6K1/versions/YTRNLDqy/voicechat-neoforge-1.21.1-2.5.28.jar"



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
    assert await fetcher.download_versions(response) != False

@pytest.mark.asyncio
async def test_download_versions():
    params = {
        'loaders' : ['neoforge'],
        'game_versions': ['1.21.1']
    }
    fetcher = FetcherModrinth(["https://modrinth.com/datapack/terralith"], params)
    responses = await fetcher.fetch_all()
    
    response = await fetcher.get_latest_version(responses)
    assert await fetcher.download_versions(response) != False

