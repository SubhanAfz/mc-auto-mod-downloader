"""
This module is responsible for fetching data from Modrinth's API.
"""
import asyncio
import ssl
import certifi
import aiohttp
from urllib.parse import urlparse

class FetcherModrinth:
    """
    Fetcher class for Modrinth API.

    Args:
        links (list): List of links to fetch data from.
        prefix (str): Prefix to add to the links (such as queries etc).
    """
    def __init__(self, links: list, prefix: str):
        # Create an SSL context using certifi's CA bundle.
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.links = self._parse_links(links)
        self.prefix = prefix


    """
    Parse the links to get the project slug and return a list of links.
    """
    def _parse_links(self, links: list) -> list:
        parsed_links = []
        for link in links:
            url = urlparse(link)
            path_parts = url.path.strip("/").split("/")
            slug = path_parts[-1]
            parsed_links.append(f'https://api.modrinth.com/v2/project/{slug}/version')
        return parsed_links
    

    """
    Fetch data from the links and return a list of responses.
    """
    async def fetch_all(self):
        async def _fetch(session: aiohttp.ClientSession ,url: str) -> dict:
            async with session.get(url, ssl=self.ssl_context) as response:
                return await response.json()
        async with aiohttp.ClientSession() as session:
            tasks = [_fetch(session, f'{url}{self.prefix}') for url in self.links]
            responses = await asyncio.gather(*tasks)
            return responses

    