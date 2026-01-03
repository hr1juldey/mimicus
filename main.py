"""Autonomous MCP client demonstration."""

import asyncio
from mcp_client import get_manager, call_tool


async def demo_autonomous_discovery():
    """Demonstrate autonomous MCP server discovery and tool calling."""
    print("\n🚀 Autonomous MCP Client")
    print("="*60)

    # Get the manager (automatically discovers all servers)
    manager = await get_manager()

    # Print summary of what was discovered
    manager.print_summary()

    # Demonstrate autonomous tool calling
    print("\n🔨 Autonomous Tool Calling Demo")
    print("="*60)

    repo_root = "/home/riju279/Documents/Tools/mimicus/mimicus"

    # Call tools without specifying server (auto-detected)
    demo_calls = [
        ("initialize_repo", {"repo_root": repo_root, "dir_name": ".claude"}),
        ("get_system_status", {"repo_root": repo_root}),
        ("add", {"a": 42, "b": 8}),
        ("multiply", {"a": 7, "b": 6}),
        ("square_root", {"x": 256}),
    ]

    for tool_name, args in demo_calls:
        try:
            print(f"\n📞 Calling: {tool_name}({args})")
            result = await call_tool(tool_name, args)

            if result.content:
                content = result.content[0].text if result.content else "No result"
                # Show limited output
                output = content if len(content) < 100 else content[:100] + "..."
                print(f"✓ Result: {output}")
        except Exception as e:
            print(f"✗ Failed: {e}")

    print(f"\n{'='*60}")
    print("✓ Autonomous demo complete!")
    print("="*60)


async def main():
    """Run autonomous MCP client."""
    await demo_autonomous_discovery()


if __name__ == "__main__":
    asyncio.run(main())