"""Remote CLI client for Compounding Engineering (CE) MCP server."""

import asyncio
import argparse
import sys
from pathlib import Path
from mcp_client import get_manager, call_tool, format_result


async def init_repo(repo_root: str, dir_name: str = ".claude") -> bool:
    """Initialize repository with compounding directory."""
    print(f"\n📦 Initializing repository: {repo_root}")
    print(f"   Directory: {dir_name}")
    print("="*60)

    try:
        result = await call_tool(
            "initialize_repo",
            {"repo_root": repo_root, "dir_name": dir_name},
            server_name="compounding-engineering"
        )

        output = format_result(result)
        print(f"✓ Repository initialized successfully!")
        print(f"\n{output}\n")
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False


async def index_codebase(
    repo_root: str, recreate: bool = False, with_graphrag: bool = False
) -> bool:
    """Index repository codebase with optional GraphRAG extraction."""
    print(f"\n🔍 Indexing codebase: {repo_root}")
    print(f"   Recreate: {recreate}")
    print(f"   GraphRAG: {with_graphrag}")
    print("="*60)

    try:
        result = await call_tool(
            "index_codebase",
            {
                "repo_root": repo_root,
                "recreate": recreate,
                "with_graphrag": with_graphrag
            },
            server_name="compounding-engineering"
        )

        output = format_result(result)
        print(f"✓ Codebase indexed successfully!")
        print(f"\n{output}\n")
        return True
    except Exception as e:
        print(f"✗ Indexing failed: {e}")
        return False


async def show_server_info() -> bool:
    """Discover and show available MCP servers and their tools."""
    print("\n📡 MCP Server Discovery")
    print("="*60)

    try:
        manager = await get_manager()
        manager.print_summary()
        return True
    except Exception as e:
        print(f"✗ Discovery failed: {e}")
        return False


async def garden_knowledge(repo_root: str, action: str = "consolidate") -> bool:
    """Maintain knowledge base."""
    print(f"\n🌱 Gardening Knowledge Base")
    print("="*60)
    print(f"Repository: {repo_root}")
    print(f"Action: {action}")
    print("="*60)

    try:
        result = await call_tool(
            "garden_knowledge",
            {
                "repo_root": repo_root,
                "action": action
            },
            server_name="compounding-engineering"
        )

        output = format_result(result)
        print(f"\n✓ Knowledge base gardened successfully!\n")
        print(output)
        print("\n" + "="*60)
        return True
    except Exception as e:
        print(f"✗ Knowledge base gardening failed: {e}")
        return False


async def generate_plan(repo_root: str, description: str) -> bool:
    """Generate implementation plan from feature description."""
    print(f"\n📋 Generating Implementation Plan")
    print("="*60)
    print(f"Repository: {repo_root}")
    print(f"Feature: {description[:80]}...")
    print("="*60)

    try:
        result = await call_tool(
            "generate_plan",
            {
                "repo_root": repo_root,
                "feature_description": description
            },
            server_name="compounding-engineering"
        )

        output = format_result(result)
        print(f"\n✓ Plan generated successfully!\n")
        print(output)
        print("\n" + "="*60)
        return True
    except Exception as e:
        print(f"✗ Plan generation failed: {e}")
        return False


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Remote CLI client for Compounding Engineering MCP server"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Initialize repo command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize repository with compounding directory"
    )
    init_parser.add_argument(
        "--repo-root",
        default="/home/riju279/Documents/Tools/mimicus/mimicus",
        help="Repository root path"
    )
    init_parser.add_argument(
        "--dir-name",
        default=".claude",
        help="Directory name for compounding data"
    )

    # Index codebase command
    index_parser = subparsers.add_parser(
        "index",
        help="Index codebase with optional GraphRAG extraction"
    )
    index_parser.add_argument(
        "--repo-root",
        default="/home/riju279/Documents/Tools/mimicus/mimicus",
        help="Repository root path"
    )
    index_parser.add_argument(
        "--recreate",
        action="store_true",
        help="Force recreation of vector collection"
    )
    index_parser.add_argument(
        "--graphrag",
        action="store_true",
        help="Enable GraphRAG entity extraction"
    )

    # Garden knowledge command
    garden_parser = subparsers.add_parser(
        "garden",
        help="Maintain and consolidate knowledge base"
    )
    garden_parser.add_argument(
        "--action",
        default="consolidate",
        choices=["consolidate", "compress-memory", "index-commits", "all"],
        help="Gardening action to perform"
    )
    garden_parser.add_argument(
        "--repo-root",
        default="/home/riju279/Documents/Tools/mimicus/mimicus",
        help="Repository root path"
    )

    # Generate plan command
    plan_parser = subparsers.add_parser(
        "generate-plan",
        help="Generate implementation plan from feature description"
    )
    plan_parser.add_argument(
        "--description",
        required=True,
        help="Feature description for plan generation"
    )
    plan_parser.add_argument(
        "--repo-root",
        default="/home/riju279/Documents/Tools/mimicus/mimicus",
        help="Repository root path"
    )

    # Servers command
    subparsers.add_parser(
        "servers",
        help="Show available MCP servers and tools"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    if args.command == "init":
        success = await init_repo(args.repo_root, args.dir_name)
        return 0 if success else 1

    elif args.command == "index":
        success = await index_codebase(
            args.repo_root,
            recreate=args.recreate,
            with_graphrag=args.graphrag
        )
        return 0 if success else 1

    elif args.command == "garden":
        success = await garden_knowledge(args.repo_root, args.action)
        return 0 if success else 1

    elif args.command == "generate-plan":
        success = await generate_plan(args.repo_root, args.description)
        return 0 if success else 1

    elif args.command == "servers":
        success = await show_server_info()
        return 0 if success else 1

    return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)