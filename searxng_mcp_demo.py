#!/usr/bin/env python3
"""
Demo MCP server that interfaces with SearXNG search engine.

This demonstrates how to create an MCP server that can be integrated with the trio.
"""

import json
from typing import Dict, Any
import aiohttp
from fastmcp import FastMCP

mcp = FastMCP("SearXNG Search Server")


async def search_web(query: str, format_type: str = "json") -> Dict[str, Any]:
    """
    Search using SearXNG API.

    Args:
        query: Search query string
        format_type: Response format ('json', 'html', etc.)

    Returns:
        Search results
    """
    searxng_url = f"http://localhost:8080/search?q={query}&format={format_type}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(searxng_url) as response:
                if response.status == 200:
                    if format_type.lower() == "json":
                        results = await response.json()
                        # Return only the top 3 results to keep response concise
                        if "results" in results:
                            results["results"] = results["results"][:3]
                        return results
                    else:
                        content = await response.text()
                        return {"content": content, "status": "success"}
                else:
                    return {"error": f"HTTP {response.status}", "status": "failed"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}


@mcp.tool(
    name="search",
    description="Search the web using SearXNG metasearch engine"
)
async def search_tool(query: str, format_type: str = "json") -> Dict[str, Any]:
    return await search_web(query, format_type)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8082)