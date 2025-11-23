# filename: app/fastmcp.py
import httpx
import logging

logger = logging.getLogger("fastmcp_client")

class FastMCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def request(self, tool_name: str, data: dict):
        """
        Sends a POST request to the MCP server.
        Assumes the server exposes a route matching the tool_name (e.g., /search_flights).
        """
        url = f"{self.base_url}/{tool_name}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                logger.info(f"POST {url} with data: {data}")
                response = await client.post(url, json=data)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            logger.error(f"Connection error to {url}: {e}")
            return [] # Return empty list on failure so the app doesn't crash
        except httpx.HTTPStatusError as e:
            logger.error(f"Server error from {url}: {e.response.text}")
            return []