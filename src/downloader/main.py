from fetcher import FetcherModrinth
from fileloader import FileLoader
import asyncio
import sys
import os

async def main():
    modstxt_path = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), sys.argv[1])
    mods_path = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), 'mods/')
    file_loader = FileLoader(modstxt_path)
    modrinth_urls = file_loader.load_file()
    params = {
        "loaders": ["neoforge"],
        "game_versions": ["1.21.1"]
    }
    fetcher = FetcherModrinth(modrinth_urls, params=params)
    print(modrinth_urls)
    responses = await fetcher.fetch_all()
    print(responses)
    latest_versions = await fetcher.get_latest_version(responses)
    print(latest_versions)
    await fetcher.download_versions(latest_versions, folder=mods_path)
    print("Downloaded versions successfully.")


if __name__ == "__main__":
    asyncio.run(main())