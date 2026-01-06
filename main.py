"""Remote CLI client for Compounding Engineering (CE) MCP server - All 16 Tools."""

import asyncio
import argparse
import sys
from mcp_client import get_manager, call_tool, format_result


def progress_handler(msg_type="general"):
    """Create a progress handler function."""

    def handler(progress, total, message):
        if message:
            if total and progress > 0:
                pct = (progress / total * 100) if total > 0 else 0
                print(f"  ⏳ [{pct:3.0f}%] {message}")
            else:
                print(f"  ℹ️  {message}")

    return handler


# ============================================================================
# REPOSITORY TOOLS
# ============================================================================


async def initialize_repo(repo_root: str, dir_name: str = ".claude") -> bool:
    """Initialize repository with compounding directory."""
    print(f"\n📦 Initializing repository: {repo_root}")
    print(f"   Directory: {dir_name}")
    print("=" * 60)

    try:
        result = await call_tool(
            "initialize_repo",
            {"repo_root": repo_root, "dir_name": dir_name},
            server_name="compounding-engineering",
        )

        output = format_result(result)
        print("✓ Repository initialized successfully!")
        print(f"\n{output}\n")
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False


async def get_repo_status(repo_root: str) -> bool:
    """Get repository status and metadata."""
    print(f"\n📊 Repository Status: {repo_root}")
    print("=" * 60)

    try:
        result = await call_tool(
            "get_repo_status",
            {"repo_root": repo_root},
            server_name="compounding-engineering",
        )

        output = format_result(result)
        print("\n✓ Repository status retrieved!")
        print(f"\n{output}\n")
        return True
    except Exception as e:
        print(f"✗ Failed to get repository status: {e}")
        return False


async def get_task_status(task_id: str) -> bool:
    """Get status of background task by ID."""
    print(f"\n⏱️  Task Status: {task_id}")
    print("=" * 60)

    try:
        result = await call_tool(
            "get_task_status",
            {"task_id": task_id},
            server_name="compounding-engineering",
        )

        output = format_result(result)
        print("\n✓ Task status retrieved!")
        print(f"\n{output}\n")
        return True
    except Exception as e:
        print(f"✗ Failed to get task status: {e}")
        return False


# ============================================================================
# KNOWLEDGE TOOLS
# ============================================================================


async def index_codebase(
    repo_root: str, recreate: bool = False, with_graphrag: bool = False
) -> bool:
    """Index repository codebase with optional GraphRAG extraction."""
    print(f"\n🔍 Indexing codebase: {repo_root}")
    print(f"   Recreate: {recreate}")
    print(f"   GraphRAG: {with_graphrag}")
    print("=" * 60)

    try:
        result = await call_tool(
            "index_codebase",
            {
                "repo_root": repo_root,
                "recreate": recreate,
                "with_graphrag": with_graphrag,
            },
            server_name="compounding-engineering",
            progress_callback=progress_handler("indexing"),
        )

        output = format_result(result)
        print("\n✓ Codebase indexed successfully!")
        print(f"\n{output}\n")
        return True
    except Exception as e:
        print(f"✗ Indexing failed: {e}")
        return False


async def garden_knowledge(repo_root: str, action: str = "consolidate") -> bool:
    """Maintain and optimize knowledge base."""
    print("\n🌱 Gardening Knowledge Base")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Action: {action}")
    print("=" * 60)

    try:
        result = await call_tool(
            "garden_knowledge",
            {"repo_root": repo_root, "action": action},
            server_name="compounding-engineering",
            progress_callback=progress_handler("garden"),
        )

        output = format_result(result)
        print("\n✓ Knowledge base gardened successfully!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Knowledge base gardening failed: {e}")
        return False


async def codify_feedback(
    repo_root: str, feedback: str, source: str = "manual_input"
) -> bool:
    """Codify feedback into knowledge base."""
    print("\n📝 Codifying Feedback")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Source: {source}")
    print(f"Feedback: {feedback[:100]}...")
    print("=" * 60)

    try:
        result = await call_tool(
            "codify_feedback",
            {"repo_root": repo_root, "feedback": feedback, "source": source},
            server_name="compounding-engineering",
            progress_callback=progress_handler("codify"),
        )

        output = format_result(result)
        print("\n✓ Feedback codified successfully!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Feedback codification failed: {e}")
        return False


async def compress_knowledge_base(
    repo_root: str, ratio: float = 0.5, dry_run: bool = False
) -> bool:
    """Compress knowledge base semantically."""
    print("\n🗜️  Compressing Knowledge Base")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Ratio: {ratio}")
    print(f"Dry Run: {dry_run}")
    print("=" * 60)

    try:
        result = await call_tool(
            "compress_knowledge_base",
            {"repo_root": repo_root, "ratio": ratio, "dry_run": dry_run},
            server_name="compounding-engineering",
            progress_callback=progress_handler("compress"),
        )

        output = format_result(result)
        print("\n✓ Knowledge base compressed successfully!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Compression failed: {e}")
        return False


# ============================================================================
# ANALYSIS TOOLS
# ============================================================================


async def analyze_code(
    repo_root: str,
    entity: str,
    analysis_type: str = "navigate",
    max_depth: int = 2,
    change_type: str = "Modify",
) -> bool:
    """Analyze code using GraphRAG agents."""
    print("\n🔬 Analyzing Code")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Entity: {entity}")
    print(f"Analysis Type: {analysis_type}")
    print(f"Max Depth: {max_depth}")
    print("=" * 60)

    try:
        result = await call_tool(
            "analyze_code",
            {
                "repo_root": repo_root,
                "entity": entity,
                "analysis_type": analysis_type,
                "max_depth": max_depth,
                "change_type": change_type,
            },
            server_name="compounding-engineering",
            progress_callback=progress_handler("analyze"),
        )

        output = format_result(result)
        print("\n✓ Code analysis complete!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Code analysis failed: {e}")
        return False


async def generate_plan(repo_root: str, description: str) -> bool:
    """Generate implementation plan from feature description."""
    print("\n📋 Generating Implementation Plan")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Feature: {description[:80]}...")
    print("=" * 60)

    try:
        result = await call_tool(
            "generate_plan",
            {
                "repo_root": repo_root,
                "feature_description": description,
            },
            server_name="compounding-engineering",
            progress_callback=progress_handler("plan"),
        )

        output = format_result(result)
        print("\n✓ Plan generated successfully!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Plan generation failed: {e}")
        return False


# ============================================================================
# EXECUTION TOOLS
# ============================================================================


async def execute_work(
    repo_root: str,
    pattern: str = None,
    dry_run: bool = False,
    parallel: bool = True,
    max_workers: int = 3,
) -> bool:
    """Execute work items (todos/plans) using ReAct agents."""
    print("\n⚙️  Executing Work")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Pattern: {pattern or 'all'}")
    print(f"Dry Run: {dry_run}")
    print(f"Mode: {'parallel' if parallel else 'sequential'}")
    print("=" * 60)

    try:
        result = await call_tool(
            "execute_work",
            {
                "repo_root": repo_root,
                "pattern": pattern,
                "dry_run": dry_run,
                "parallel": parallel,
                "max_workers": max_workers,
            },
            server_name="compounding-engineering",
            progress_callback=progress_handler("work"),
        )

        output = format_result(result)
        print("\n✓ Work execution complete!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Work execution failed: {e}")
        return False


async def review_code(
    repo_root: str, pr_url_or_id: str = "latest", project: bool = False
) -> bool:
    """Perform exhaustive multi-agent code review."""
    print("\n👀 Code Review")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Target: {pr_url_or_id}")
    print(f"Scope: {'entire project' if project else 'PR/branch'}")
    print("=" * 60)

    try:
        result = await call_tool(
            "review_code",
            {
                "repo_root": repo_root,
                "pr_url_or_id": pr_url_or_id,
                "project": project,
            },
            server_name="compounding-engineering",
            progress_callback=progress_handler("review"),
        )

        output = format_result(result)
        print("\n✓ Code review complete!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Code review failed: {e}")
        return False


async def check_policies(
    repo_root: str, paths: list = None, auto_fix: bool = False
) -> bool:
    """Check policy compliance."""
    print("\n✅ Checking Policies")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Paths: {paths or 'all'}")
    print(f"Auto Fix: {auto_fix}")
    print("=" * 60)

    try:
        result = await call_tool(
            "check_policies",
            {
                "repo_root": repo_root,
                "paths": paths,
                "auto_fix": auto_fix,
            },
            server_name="compounding-engineering",
        )

        output = format_result(result)
        print("\n✓ Policy check complete!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Policy check failed: {e}")
        return False


# ============================================================================
# SYSTEM TOOLS
# ============================================================================


async def triage_issues(
    repo_root: str, pattern: str = None, dry_run: bool = False
) -> bool:
    """Triage and categorize codebase issues."""
    print("\n🏷️  Triaging Issues")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Pattern: {pattern or 'all'}")
    print(f"Dry Run: {dry_run}")
    print("=" * 60)

    try:
        result = await call_tool(
            "triage_issues",
            {
                "repo_root": repo_root,
                "pattern": pattern,
                "dry_run": dry_run,
            },
            server_name="compounding-engineering",
            progress_callback=progress_handler("triage"),
        )

        output = format_result(result)
        print("\n✓ Issue triage complete!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Issue triage failed: {e}")
        return False


async def generate_command(
    repo_root: str, description: str, dry_run: bool = False
) -> bool:
    """Generate CLI command from natural language description."""
    print("\n🛠️  Generating Command")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Description: {description[:80]}...")
    print(f"Dry Run: {dry_run}")
    print("=" * 60)

    try:
        result = await call_tool(
            "generate_command",
            {
                "repo_root": repo_root,
                "description": description,
                "dry_run": dry_run,
            },
            server_name="compounding-engineering",
            progress_callback=progress_handler("command"),
        )

        output = format_result(result)
        print("\n✓ Command generated successfully!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Command generation failed: {e}")
        return False


async def get_system_status(repo_root: str) -> bool:
    """Get system diagnostics."""
    print("\n🔧 System Status")
    print("=" * 60)

    try:
        result = await call_tool(
            "get_system_status",
            {"repo_root": repo_root},
            server_name="compounding-engineering",
        )

        output = format_result(result)
        print("\n✓ System status retrieved!\n")
        print(output)
        print("\n" + "=" * 60)
        return True
    except Exception as e:
        print(f"✗ Failed to get system status: {e}")
        return False


async def show_server_info() -> bool:
    """Discover and show available MCP servers and their tools."""
    print("\n📡 MCP Server Discovery")
    print("=" * 60)

    try:
        manager = await get_manager()
        manager.print_summary()
        return True
    except Exception as e:
        print(f"✗ Discovery failed: {e}")
        return False


# ============================================================================
# MAIN CLI
# ============================================================================


async def main():
    """Main CLI entry point with all 16 tools."""
    parser = argparse.ArgumentParser(
        description="Remote CLI client for Compounding Engineering MCP server (All 16 Tools)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Repository commands
    init_parser = subparsers.add_parser("init", help="Initialize repository")
    init_parser.add_argument("--repo-root", required=True, help="Repository root path")
    init_parser.add_argument("--dir-name", default=".claude", help="Directory name")

    status_parser = subparsers.add_parser("status", help="Get repository status")
    status_parser.add_argument(
        "--repo-root", required=True, help="Repository root path"
    )

    task_parser = subparsers.add_parser("task-status", help="Get task status")
    task_parser.add_argument("--task-id", required=True, help="Task ID")

    # Knowledge commands
    index_parser = subparsers.add_parser("index", help="Index codebase")
    index_parser.add_argument("--repo-root", required=True, help="Repository root path")
    index_parser.add_argument(
        "--recreate", action="store_true", help="Recreate collection"
    )
    index_parser.add_argument("--graphrag", action="store_true", help="Enable GraphRAG")

    garden_parser = subparsers.add_parser("garden", help="Maintain knowledge base")
    garden_parser.add_argument(
        "--repo-root", required=True, help="Repository root path"
    )
    garden_parser.add_argument(
        "--action",
        default="consolidate",
        choices=["consolidate", "compress-memory", "index-commits", "all"],
        help="Action to perform",
    )

    codify_parser = subparsers.add_parser("codify", help="Codify feedback")
    codify_parser.add_argument(
        "--repo-root", required=True, help="Repository root path"
    )
    codify_parser.add_argument("--feedback", required=True, help="Feedback text")
    codify_parser.add_argument(
        "--source", default="manual_input", help="Feedback source"
    )

    compress_parser = subparsers.add_parser("compress", help="Compress knowledge base")
    compress_parser.add_argument(
        "--repo-root", required=True, help="Repository root path"
    )
    compress_parser.add_argument(
        "--ratio", type=float, default=0.5, help="Compression ratio"
    )
    compress_parser.add_argument("--dry-run", action="store_true", help="Preview only")

    # Analysis commands
    analyze_parser = subparsers.add_parser("analyze", help="Analyze code")
    analyze_parser.add_argument(
        "--repo-root", required=True, help="Repository root path"
    )
    analyze_parser.add_argument("--entity", required=True, help="Entity to analyze")
    analyze_parser.add_argument("--type", default="navigate", help="Analysis type")
    analyze_parser.add_argument("--depth", type=int, default=2, help="Max depth")
    analyze_parser.add_argument("--change-type", default="Modify", help="Change type")

    plan_parser = subparsers.add_parser("plan", help="Generate implementation plan")
    plan_parser.add_argument("--repo-root", required=True, help="Repository root path")
    plan_parser.add_argument("--description", required=True, help="Feature description")

    # Execution commands
    work_parser = subparsers.add_parser("execute", help="Execute work items")
    work_parser.add_argument("--repo-root", required=True, help="Repository root path")
    work_parser.add_argument("--pattern", help="Work item pattern")
    work_parser.add_argument("--dry-run", action="store_true", help="Preview only")
    work_parser.add_argument(
        "--sequential", action="store_true", help="Sequential mode"
    )
    work_parser.add_argument("--max-workers", type=int, default=3, help="Max workers")

    review_parser = subparsers.add_parser("review", help="Review code")
    review_parser.add_argument(
        "--repo-root", required=True, help="Repository root path"
    )
    review_parser.add_argument("--pr", default="latest", help="PR ID or URL")
    review_parser.add_argument(
        "--project", action="store_true", help="Review entire project"
    )

    policy_parser = subparsers.add_parser(
        "check-policies", help="Check policy compliance"
    )
    policy_parser.add_argument(
        "--repo-root", required=True, help="Repository root path"
    )
    policy_parser.add_argument(
        "--auto-fix", action="store_true", help="Auto-fix violations"
    )

    # System commands
    triage_parser = subparsers.add_parser("triage", help="Triage issues")
    triage_parser.add_argument(
        "--repo-root", required=True, help="Repository root path"
    )
    triage_parser.add_argument("--pattern", help="Issue pattern")
    triage_parser.add_argument("--dry-run", action="store_true", help="Preview only")

    cmd_parser = subparsers.add_parser("gen-command", help="Generate CLI command")
    cmd_parser.add_argument("--repo-root", required=True, help="Repository root path")
    cmd_parser.add_argument("--description", required=True, help="Command description")
    cmd_parser.add_argument("--dry-run", action="store_true", help="Preview only")

    sys_parser = subparsers.add_parser("sys-status", help="Get system diagnostics")
    sys_parser.add_argument("--repo-root", required=True, help="Repository root path")

    # Discovery command
    subparsers.add_parser("servers", help="Show available MCP servers and tools")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    if args.command == "init":
        success = await initialize_repo(args.repo_root, args.dir_name)
        return 0 if success else 1

    elif args.command == "status":
        success = await get_repo_status(args.repo_root)
        return 0 if success else 1

    elif args.command == "task-status":
        success = await get_task_status(args.task_id)
        return 0 if success else 1

    elif args.command == "index":
        success = await index_codebase(
            args.repo_root, recreate=args.recreate, with_graphrag=args.graphrag
        )
        return 0 if success else 1

    elif args.command == "garden":
        success = await garden_knowledge(args.repo_root, args.action)
        return 0 if success else 1

    elif args.command == "codify":
        success = await codify_feedback(args.repo_root, args.feedback, args.source)
        return 0 if success else 1

    elif args.command == "compress":
        success = await compress_knowledge_base(
            args.repo_root, args.ratio, args.dry_run
        )
        return 0 if success else 1

    elif args.command == "analyze":
        success = await analyze_code(
            args.repo_root,
            args.entity,
            args.type,
            args.depth,
            args.change_type,
        )
        return 0 if success else 1

    elif args.command == "plan":
        success = await generate_plan(args.repo_root, args.description)
        return 0 if success else 1

    elif args.command == "execute":
        success = await execute_work(
            args.repo_root,
            args.pattern,
            args.dry_run,
            parallel=not args.sequential,
            max_workers=args.max_workers,
        )
        return 0 if success else 1

    elif args.command == "review":
        success = await review_code(args.repo_root, args.pr, args.project)
        return 0 if success else 1

    elif args.command == "check-policies":
        success = await check_policies(args.repo_root, auto_fix=args.auto_fix)
        return 0 if success else 1

    elif args.command == "triage":
        success = await triage_issues(args.repo_root, args.pattern, args.dry_run)
        return 0 if success else 1

    elif args.command == "gen-command":
        success = await generate_command(args.repo_root, args.description, args.dry_run)
        return 0 if success else 1

    elif args.command == "sys-status":
        success = await get_system_status(args.repo_root)
        return 0 if success else 1

    elif args.command == "servers":
        success = await show_server_info()
        return 0 if success else 1

    return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
