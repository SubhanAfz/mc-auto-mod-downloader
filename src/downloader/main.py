from fetcher import FetcherModrinth
from fileloader import FileLoader
import asyncio

async def main():
    file_loader = FileLoader()
    links = file_loader.load_file()
    params = {
        'loaders' : ['neoforge'],
        'game_versions': ['1.21.1']
    }
    fetcher = FetcherModrinth(links,params)
    responses = await fetcher.fetch_all()
    versions = await fetcher.get_latest_version(responses)

    

    print(versions)

if __name__ == "__main__":
    asyncio.run(main())