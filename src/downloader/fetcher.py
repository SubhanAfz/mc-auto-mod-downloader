"""
This module is responsible for fetching data from Modrinth's API.
"""
import asyncio
import ssl
import certifi
import aiohttp
from urllib.parse import urlparse
import os

class FetcherModrinth:
    """
    Fetcher class for Modrinth API.

    Args:
        links (list): List of links to fetch data from.
        params (dict): Query parameters to append to the links.
    """
    def __init__(self, links: list, params=None) -> None:
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
    async def fetch_all(self) -> list:
        async def _fetch(session: aiohttp.ClientSession ,url: str) -> dict:
            async with session.get(url, ssl=self.ssl_context) as response:
                return await response.json()
        async with aiohttp.ClientSession() as session:
            tasks = [_fetch(session, url) for url in self.links]
            responses = await asyncio.gather(*tasks)
            return responses
        
    
    """
    Get the versions from the response and return a list of versions.

    Args:
        response (dict): Response from the API.
    """
    async def _filter_versions(self, responses: list[dict]) -> list:
        filtered = []
        for version in responses:
            if all(game_version in self.params["game_versions"] for game_version in version["game_versions"]) and all(loader in self.params["loaders"] for loader in version["loaders"]):
                filtered.append(True)
            else:
                filtered.append(False)
        return filtered
    

    """
    Get the latest version from the responses and return a list of versions.
    
    Args:
        responses (list): List of responses from the API.
    """
    async def get_latest_version(self, responses: list[dict]) -> dict:
        tasks = [self._filter_versions(response) for response in responses]
        r = await asyncio.gather(*tasks)
        latest_versions = []
        for i, r_s in enumerate(r):
            for j, success in enumerate(r_s):
                if success:
                    latest_versions.append(responses[i][j])
                    break
        return latest_versions

                    
    async def _download_version(self, response: dict, folder="./") -> bool:
        if not response:
            return None
        url = response["files"][0]["url"]
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=self.ssl_context) as resp:
                if resp.status != 200:
                    return False
                
                file = response["files"][0]["filename"]
                os.makedirs(folder, exist_ok=True)
                file = os.path.join(folder, file)
                with open(file, "wb") as f:
                    f.write(await resp.read())
                
                return True
    
    async def download_versions(self, responses: list[dict], folder="./") -> bool:
        if not responses:
            return None
        tasks = [self._download_version(response, folder) for response in responses]
        return await asyncio.gather(*tasks)