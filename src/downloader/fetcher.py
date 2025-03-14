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
        params (dict): Query parameters to append to the links.
    """
    def __init__(self, links: list, params: dict):
        # Create an SSL context using certifi's CA bundle.
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.links = self._parse_links(links)
        self.params = params

    """
    Parse the links to get the project slug and return a list of links.

    Args:
        links (list): List of links to parse.

    Returns:
        list: List of parsed links.
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
            tasks = [_fetch(session, url) for url in self.links]
            responses = await asyncio.gather(*tasks)
            return responses
    
    """
    Get the latest version from the responses and return a list of versions.
    
    Args:
        responses (list): List of responses from the API.
    """
    async def get_latest_version(self, responses):
        async def _get_latest_version(response):
            # Check if the version is a release.
            filtered = response
            if self.params["game_versions"]:
                filtered = [
                    v for v in filtered
                    if any(gv in v.get("game_versions", []) for gv in self.params["game_versions"])
                ]
            if self.params["loaders"]:
                filtered = [
                    v for v in filtered
                    if any(loader in v.get("loaders", []) for loader in self.params["loaders"])
                ]
            return filtered
        tasks = [_get_latest_version(response) for response in responses]
        return await asyncio.gather(*tasks)
    