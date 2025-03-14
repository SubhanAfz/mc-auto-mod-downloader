from fetcher import FetcherModrinth
from fileloader import FileLoader
import asyncio

async def main():
    file_loader = FileLoader()
    links = file_loader.load_file()
    fetcher = FetcherModrinth(links, "")
    responses = await fetcher.fetch_all()
    print(responses)

if __name__ == "__main__":
    asyncio.run(main())