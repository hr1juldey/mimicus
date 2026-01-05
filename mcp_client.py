"""Autonomous MCP client for discovering and calling remote MCP servers."""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from fastmcp import Client

logger = logging.getLogger(__name__)


@dataclass
class ServerInfo:
    """Information about an MCP server."""

    name: str
    url: str
    tools: dict[str, Any] = None
    resources: dict[str, Any] = None
    prompts: dict[str, Any] = None

    def __post_init__(self):
        """Initialize empty dicts if not provided."""
        if self.tools is None:
            self.tools = {}
        if self.resources is None:
            self.resources = {}
        if self.prompts is None:
            self.prompts = {}


class MCPClientManager:
    """Manages autonomous MCP client discovery and tool calling."""

    def __init__(self, config_path: Path = Path(".mcp.json")):
        """Initialize MCP client manager."""
        self.config_path = config_path
        self.servers: dict[str, ServerInfo] = {}
        self._discovered = False

    def load_config(self) -> dict[str, Any]:
        """Load MCP servers from config file."""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return {}

        with open(self.config_path) as f:
            config = json.load(f)
        return config.get("mcpServers", {})

    async def discover_all_servers(
        self, verbose: bool = False
    ) -> dict[str, ServerInfo]:
        """Discover all configured MCP servers and their capabilities."""
        config = self.load_config()

        if not config:
            logger.error("No MCP servers configured")
            return {}

        if verbose:
            print(f"\n🔍 Discovering {len(config)} MCP server(s)...")

        for name, server_config in config.items():
            # Support both "url" and "httpUrl" formats
            url = server_config.get("httpUrl") or server_config.get("url")
            if not url:
                logger.warning(f"No URL for server: {name}")
                continue

            server_info = ServerInfo(name=name, url=url)
            await self._discover_server(server_info, verbose=verbose)
            self.servers[name] = server_info

        self._discovered = True
        if verbose:
            print(f"✓ Discovery complete! Found {len(self.servers)} server(s)\n")

        return self.servers

    async def _discover_server(self, server: ServerInfo, verbose: bool = False) -> None:
        """Discover capabilities of a single server."""
        client = Client(server.url)

        try:
            async with client:
                if verbose:
                    print(f"\n📡 {server.name} ({server.url})")

                # Test connectivity
                await client.ping()
                if verbose:
                    print("  ✓ Connected")

                # Discover tools
                tools = await client.list_tools()
                for tool in tools:
                    server.tools[tool.name] = {
                        "description": tool.description,
                        "input_schema": tool.inputSchema,
                    }
                if verbose and tools:
                    print(f"  • {len(tools)} tool(s)")

                # Discover resources
                resources = await client.list_resources()
                for resource in resources:
                    server.resources[resource.uri] = {
                        "description": resource.description
                    }
                if verbose and resources:
                    print(f"  • {len(resources)} resource(s)")

                # Discover prompts
                prompts = await client.list_prompts()
                for prompt in prompts:
                    server.prompts[prompt.name] = {"description": prompt.description}
                if verbose and prompts:
                    print(f"  • {len(prompts)} prompt(s)")

        except Exception as e:
            logger.error(f"Failed to discover {server.name}: {e}")

    async def call_tool(
        self, tool_name: str, args: dict[str, Any], server_name: Optional[str] = None
    ) -> Any:
        """Call a tool on any discovered server."""
        if not self._discovered:
            await self.discover_all_servers()

        # If server name not specified, find it
        if not server_name:
            server_name = self._find_server_with_tool(tool_name)
            if not server_name:
                raise ValueError(f"Tool not found: {tool_name}")

        server = self.servers.get(server_name)
        if not server:
            raise ValueError(f"Server not found: {server_name}")

        if tool_name not in server.tools:
            raise ValueError(f"Tool '{tool_name}' not found on server '{server_name}'")

        client = Client(server.url)
        try:
            async with client:
                result = await client.call_tool(tool_name, args)
                return result
        except Exception as e:
            logger.error(f"Failed to call {tool_name} on {server_name}: {e}")
            raise

    def _find_server_with_tool(self, tool_name: str) -> Optional[str]:
        """Find which server has a specific tool."""
        for server_name, server in self.servers.items():
            if tool_name in server.tools:
                return server_name
        return None

    def get_server_tools(self, server_name: str) -> dict[str, Any]:
        """Get all tools for a server."""
        server = self.servers.get(server_name)
        return server.tools if server else {}

    def get_all_tools(self) -> dict[str, list[str]]:
        """Get all tools grouped by server."""
        return {
            name: list(server.tools.keys()) for name, server in self.servers.items()
        }

    def print_summary(self) -> None:
        """Print a summary of discovered servers and tools."""
        if not self.servers:
            print("No servers discovered")
            return

        print("\n" + "=" * 60)
        print("MCP SERVERS SUMMARY")
        print("=" * 60)

        for server_name, server in self.servers.items():
            print(f"\n📡 {server_name}")
            print(f"   URL: {server.url}")
            if server.tools:
                print(f"   Tools ({len(server.tools)}):")
                for tool_name in sorted(server.tools.keys()):
                    print(f"     • {tool_name}")
            if server.resources:
                print(f"   Resources ({len(server.resources)}):")
                for resource_uri in sorted(server.resources.keys()):
                    print(f"     • {resource_uri}")
            if server.prompts:
                print(f"   Prompts ({len(server.prompts)}):")
                for prompt_name in sorted(server.prompts.keys()):
                    print(f"     • {prompt_name}")

        print("\n" + "=" * 60)


# Global manager instance
_manager: Optional[MCPClientManager] = None


async def get_manager() -> MCPClientManager:
    """Get or create the global MCP manager."""
    global _manager
    if _manager is None:
        _manager = MCPClientManager()
        await _manager.discover_all_servers(verbose=True)
    return _manager


async def call_tool(
    tool_name: str, args: dict[str, Any], server_name: Optional[str] = None
) -> Any:
    """Convenience function to call a tool without explicit manager."""
    manager = await get_manager()
    return await manager.call_tool(tool_name, args, server_name)


def print_servers_summary() -> None:
    """Print summary of discovered servers (sync wrapper)."""
    if _manager:
        _manager.print_summary()


def format_result(result: Any) -> str:
    """Format MCP tool call result for display."""
    if not result:
        return "No result returned"

    # Handle content-based results (standard MCP response format)
    if hasattr(result, "content") and result.content:
        contents = []
        for item in result.content:
            if hasattr(item, "text"):
                contents.append(item.text)
            else:
                contents.append(str(item))
        return "\n".join(contents)

    # Handle dict-based results
    if isinstance(result, dict):
        import json

        try:
            return json.dumps(result, indent=2)
        except Exception:
            return str(result)

    # Fallback to string representation
    return str(result)
