# filename: app/travel_gateways.py

import logging
from app.fastmcp import FastMCPClient

from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# --- MCP Client Initialization ---
# These connect to your new servers
try:
    flight_client = FastMCPClient("http://127.0.0.1:9001")
    hotel_client = FastMCPClient("http://127.0.0.1:9002")
    train_client = FastMCPClient("http://127.0.0.1:9003")
    logger.info("MCP clients initialized.")
except Exception as e:
    logger.error(f"Failed to initialize MCP clients: {e}")
    raise

# --- MCP-Based Search Functions ---

async def search_flights(request_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Searches for flights using the Flight MCP server."""
    try:
        logger.info(f"Calling Flight MCP Server with: {request_data}")
        # The tool name 'search_flights' must match the @mcp.tool() in flight_server.py
        response = await flight_client.request("search_flights", request_data)
        return response
    except Exception as e:
        logger.error(f"Error calling Flight MCP Server: {e}")
        return []

async def search_hotels(request_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Searches for hotels using the Hotel MCP server."""
    try:
        logger.info(f"Calling Hotel MCP Server with: {request_data}")
        # The tool name 'search_hotels' must match the @mcp.tool() in hotel_server.py
        response = await hotel_client.request("search_hotels", request_data)
        return response
    except Exception as e:
        logger.error(f"Error calling Hotel MCP Server: {e}")
        return []

async def search_trains(request_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Searches for trains using the Train MCP server."""
    try:
        logger.info(f"Calling Train MCP Server with: {request_data}")
        # The tool name 'search_trains' must match the @mcp.tool() in train_server.py
        response = await train_client.request("search_trains", request_data)
        return response
    except Exception as e:
        logger.error(f"Error calling Train MCP Server: {e}")
        return []