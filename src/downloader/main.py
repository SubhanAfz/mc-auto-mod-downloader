from fetcher import FetcherModrinth
from fileloader import FileLoader
import asyncio
import sys
import os

async def main():
    file_path = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), sys.argv[1])
    file_loader = FileLoader(file_path)
    modrinth_urls = file_loader.load_file()
    params = {
        "loaders": ["neoforge"],
        "game_versions": ["1.21.1"]
    }
    fetcher = FetcherModrinth(modrinth_urls, params=params)
    responses = await fetcher.fetch_all()
    latest_versions = await fetcher.get_latest_version(responses)
    await fetcher.download_versions(latest_versions, folder="./mods")
    print("Downloaded versions successfully.")


if __name__ == "__main__":
    asyncio.run(main())