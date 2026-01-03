# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Mimicus** is a FastAPI-based universal mock & mimic service designed to mock and mimic any HTTP API for frontend engineers and integration teams when the real backend is unavailable. It supports configurable mock definitions, dynamic templating, record/replay, OpenAPI import, and stateful flows with a REST admin API and UI.

## Environment Setup

**Python Version**: 3.12

**Environment Configuration**:
- Configuration directory (Qwen): `.qwen` (controlled by `COMPOUNDING_DIR_NAME` in `.env`)
- Dependencies use `uv` package manager with lockfile (`uv.lock`)
- Project uses `pyproject.toml` for configuration and dependency management

## Development Commands

### Project Setup

```bash
# Install dependencies using uv
uv sync

# Activate virtual environment
source .venv/bin/activate  # on Linux/macOS
.venv\Scripts\activate  # on Windows
```

### Running the Application

```bash
# Run the FastMCP server (main entry point)
python main.py

# The server connects to HTTP MCP server at http://0.0.0.0:12001/mcp
```

### Code Quality & Formatting

```bash
# Format code with Black
black src/

# Lint with Ruff
ruff check src/

# Type checking with MyPy
mypy src/

# Combined quality check
black src/ && ruff check src/ && mypy src/
```

### Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run tests in async mode (project uses pytest-asyncio)
pytest -v

# Run a specific test
pytest tests/path/to/test_file.py::test_function_name
```

## Architecture Overview

The codebase follows a **modular, layered architecture** with clear separation of concerns:

### Core Layers

1. **Domain Layer** — Contains business logic entities (MockDefinition, MatchCriteria, ResponseConfig) and core domain logic for matching and response generation
2. **Application Layer** — Use cases, services, and data transfer objects (DTOs)
3. **Infrastructure Layer** — Database persistence (SQLModel/SQLAlchemy), cache (Redis), external API clients (aiohttp, httpx)
4. **Presentation Layer** — FastAPI endpoints and response serialization
5. **Config Layer** — Settings (Pydantic), environment configuration, template engine setup

### Key Components

- **FastAPI Mock Engine** — HTTP entry point handling incoming requests and returning mock/proxied responses
- **Admin API** — REST endpoints for CRUD on mock definitions, imports, and toggles
- **Config Store** — Persisted mock definitions (SQLModel/PostgreSQL or SQLite) and ephemeral state (Redis)
- **Template Engine** — Jinja2 for dynamic response templating with request variables and helpers
- **Matcher/Router** — Runtime matcher to find best mock rule for incoming requests (supports method, path, headers, query, body matching)
- **Observability** — Structured logging (structlog, loguru), Prometheus metrics, OpenTelemetry instrumentation

### Request Flow

Incoming request → Matcher finds best mock rule → Rule defines: static/template response OR proxy-to-backend → Apply response modifiers (delay, headers, status) → Persist state if configured → Return response

## Code Quality Standards

### SOLID Principles

All code must follow SOLID principles:

- **Single Responsibility Principle (SRP)**: Each class and module should have one reason to change
- **Open/Closed Principle (OCP)**: Open for extension, closed for modification
- **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types
- **Interface Segregation Principle (ISP)**: Clients shouldn't depend on interfaces they don't use
- **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concrete implementations

### File Size Constraints

- **Maximum 100 lines per Python file** (excluding test files)
- **Maximum 50 lines of overhead** (comments, imports, blank lines)
- Test files are exempt from line limits
- This enforces maintainable, focused modules that follow SOLID principles

### DRY Principle

- Every piece of logic should have a single, unambiguous representation
- Extract common code into reusable functions and classes
- Use configuration files for repeated values

### Domain-Driven Design (DDD)

- Focus on core domain logic
- Use ubiquitous language consistently
- Define clear bounded contexts with their own domain models
- Implement entities, value objects, aggregates, repositories, and services appropriately

## Standardized Variable Names

All parameters and variable names must follow conventions defined in `docs/VARIABLE_NAMES.md` to prevent incorrect data passing. Key categories include:

- Mock definition variables: `mock_id`, `mock_name`, `mock_priority`, `mock_enabled`
- Matching variables: `match_method`, `match_path`, `match_headers`, `match_query`, `match_body`
- Response variables: `response_status`, `response_headers`, `response_body`, `response_delay_ms`
- Request context: `request_method`, `request_path`, `request_headers`, `request_body`
- State variables: `state_persist_to`, `state_keys`, `session_id`
- Configuration: `config_database_url`, `config_redis_url`
- Service variables: `matching_service`, `response_service`
- HTTP client: `http_client`, `upstream_url`, `proxy_headers`

## Design Patterns

### Recommended Patterns

- **Repository Pattern** — Data access operations in domain layer
- **Service Layer Pattern** — Business logic encapsulation
- **DTO Pattern** — Data transfer between layers
- **Factory Pattern** — Creating complex objects
- **Strategy Pattern** — Different algorithm implementations
- **Observer Pattern** — Event handling

### Anti-Patterns to Avoid

- **God Objects** — Classes doing too much (SRP violation)
- **Spaghetti Code** — Tightly coupled, hard-to-follow logic
- **Magic Numbers/Strings** — Hardcoded values without explanation
- **Deep Nesting** — Excessive indentation levels
- **Premature Optimization** — Optimizing before measuring performance
- **Reinventing the Wheel** — Custom solutions when good libraries exist

## Key Dependencies

### Web Framework & MCP

- **FastAPI** (0.110.0+) — Async web framework
- **Uvicorn** — ASGI server
- **FastMCP** (2.14.2+) — Model Context Protocol integration for mock service configuration

### Data & ORM

- **SQLModel** — SQL database ORM with Pydantic validation
- **SQLAlchemy** (2.0.27+) — Core ORM layer
- **Alembic** — Database migrations
- **aiosqlite** — Async SQLite support
- **psycopg2-binary** — PostgreSQL adapter

### Caching & State

- **Redis** (5.0.3+) — Caching and ephemeral state
- **fakeredis** (2.21.0+) — Redis mock for testing

### HTTP & Templating

- **aiohttp** (3.9.0+) — Async HTTP client
- **httpx** (0.27.0+) — Modern HTTP client
- **Jinja2** (3.1.3+) — Template engine for dynamic responses
- **faker** (24.0.0+) — Fake data generation

### Matching & Validation

- **jsonpath-ng** — JSONPath querying for body matching
- **regex** — Advanced regex matching
- **jsonschema** — JSON schema validation
- **openapi-schema-validator** — OpenAPI spec validation

### Auth & Security

- **python-jose** — JWT token handling
- **passlib[bcrypt]** — Password hashing
- **bcrypt** — Password encryption

### Rate Limiting & Reliability

- **slowapi** — Rate limiting
- **tenacity** — Retry logic with exponential backoff
- **anyio** — Async compatibility layer

### Observability

- **structlog** (24.1.0+) — Structured logging
- **loguru** (0.7.2+) — Enhanced logging
- **prometheus-client** — Metrics export
- **OpenTelemetry** (api, sdk, FastAPI & httpx instrumentation) — Distributed tracing

### CLI & Development

- **Typer** — CLI framework
- **Rich** — Terminal output formatting
- **pytest** (8.1.1+) — Testing framework
- **pytest-asyncio** — Async test support
- **pytest-cov** — Coverage reporting
- **Black** — Code formatter
- **Ruff** — Fast linter
- **MyPy** — Type checker

## Documentation

Key design documents in `docs/`:

- **HLD.md** — High-level design covering feasibility, architecture, goals, data models, configuration formats, security, and deployment strategies
- **LLD.md** — Low-level design with module structure and implementation details
- **VARIABLE_NAMES.md** — Standardized naming conventions for all parameter and variable types

Additional context:
- **QWEN.md** — Qwen/CompoundingAI context with code quality standards and examples
- **README.md** — Project overview (currently minimal)

## Configuration & Environment

- Uses `pydantic-settings` for environment-based configuration
- `python-dotenv` for loading `.env` files
- YAML support via `PyYAML` for mock definitions
- FastMCP for defining and configuring mock services via HTTP protocol

## Security Considerations

- Input validation at all entry points (request headers, body, query)
- Authentication/authorization for admin endpoints (JWT via python-jose)
- Domain whitelisting for proxy operations (prevent SSRF)
- Template escaping for Jinja2 rendering (prevent injection)
- Sandboxed code execution (RestrictedPython for advanced logic)

## Testing Strategy

- **Unit tests** — Business logic components
- **Integration tests** — API endpoints
- **Contract tests** — OpenAPI specification compliance
- **End-to-end tests** — Critical user flows
- Mock Redis (fakeredis) for testing cache behavior

## Performance Considerations

- Async/await throughout for I/O operations (database, cache, HTTP)
- Connection pooling for database and Redis
- Template compilation and caching
- Efficient request matching with indexed lookups
- Rate limiting via slowapi
- Graceful degradation with fallbacks and retry logic (tenacity)

## File Structure

The project uses a modular structure (src/ is currently empty but follows the layered architecture pattern):

```
mimicus/
├── src/               # Main application code (modular layers)
├── tests/             # Test files
├── docs/              # Design documents (HLD, LLD, Variable Names)
├── main.py            # FastMCP client entry point
├── pyproject.toml     # Project configuration and dependencies
├── requirements.txt   # Readable dependency list with categories
├── uv.lock            # Dependency lock file (managed by uv)
├── .env               # Environment configuration
├── .mcp.json          # MCP servers configuration
└── QWEN.md            # Qwen/CompoundingAI context
```

## Important Notes

1. **src/ directory is empty** — The codebase is currently in early stages. Follow the architectural patterns and coding standards outlined above when adding new modules.

2. **FastMCP Integration** — The project integrates FastMCP for defining mock services via HTTP MCP protocol (configured in `.mcp.json`).

3. **Python 3.12+ Required** — Project uses modern Python features; ensure 3.12+ for development.

4. **Async-First Design** — All I/O operations should be async. Use `asyncio`, `aiohttp`, `aiosqlite`, and async SQLAlchemy sessions.

5. **Module Size Discipline** — Strictly enforce 100-line module limit. Break large features into smaller, focused modules that each handle one responsibility.

6. **Standardized Names** — Use variable naming conventions from `docs/VARIABLE_NAMES.md` consistently. This prevents subtle bugs from parameter confusion.

## Common Development Tasks

### Adding a New Mock Route

1. Create domain entities in the domain layer (matching criteria, response config)
2. Implement service logic in application layer
3. Create API endpoint in presentation layer
4. Write tests for each layer
5. Update documentation if adding new matching capabilities

### Extending Template Engine

1. Add new template filters/globals in infrastructure layer
2. Create tests for filter functionality
3. Document available template variables and helpers

### Adding Database Migrations

```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Debugging

- Enable structured logging via loguru/structlog configuration
- Use pytest with `-v` and `-s` flags for verbose output
- Check OpenTelemetry traces for request flow visualization
- Monitor Redis operations via redis-cli if using Redis caching
