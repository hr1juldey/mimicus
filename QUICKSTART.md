# Mimicus Quick Start Guide

## Stage 1 - LIVE ✅

A working FastAPI mock server with request matching and static response generation.

## Installation & Setup

```bash
# Install dependencies with uv
uv sync

# Activate virtual environment
source .venv/bin/activate
```

## Running the Server

```bash
# Start the mock server on port 18000
uv run python -m src.main

# Or with custom port
export MOCK_SERVER_PORT=8000 && uv run python -m src.main
```

The server will be available at `http://localhost:18000`

## Health Check

```bash
curl http://localhost:18000/health
# Response: {"status":"healthy","service":"mimicus","version":"0.1.0"}
```

## Testing

```bash
# Run all tests
pytest

# Run Stage 1 tests specifically
pytest tests/test_stage1_integration.py -v

# Run with coverage
pytest --cov=src tests/
```

## Example: Create and Test a Mock

```python
import asyncio
from src.domain.entities.mock_definition import MockDefinition, MatchCriteria, ResponseConfig
from src.core.dependencies import get_mock_repository

async def create_test_mock():
    repo = get_mock_repository()

    # Create a mock
    mock = MockDefinition(
        mock_id="users-list",
        mock_name="Get Users API",
        mock_priority=100,
        mock_match=MatchCriteria(
            match_method="GET",
            match_path="/api/users"
        ),
        mock_response=ResponseConfig(
            response_status=200,
            response_headers={"Content-Type": "application/json"},
            response_body='{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}'
        )
    )

    await repo.create(mock)
    print(f"Created mock: {mock.mock_name}")

# Run it
asyncio.run(create_test_mock())
```

Then test it:
```bash
curl http://localhost:18000/api/users
# Response: {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
```

## Features Available in Stage 1

### ✅ Request Matching
- Exact path matching: `/api/users` → `/api/users`
- Template paths: `/api/users/{id}` → `/api/users/123` (extracts id=123)
- HTTP method matching: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- Priority-based selection (higher priority wins)

### ✅ Response Generation
- Custom HTTP status codes
- Custom response headers
- JSON and string response bodies
- Configurable response delays (milliseconds)

### ✅ Architecture
- 5-layer modular design
- Full async/await support
- Dependency injection
- Type-safe with full type hints
- All modules <100 lines

## Coming in Stage 2

- 🔄 **Template Engine** - Dynamic responses with Jinja2
- Request variable interpolation (headers, query, path params, JSON body)
- Template helper functions (random_token, faker, timestamps)

## Coming in Stage 3

- 📝 **Admin REST API** - CRUD operations for mocks
- JSON file loading/import
- Mock enable/disable toggling
- Bulk mock operations

## Coming in Stage 4

- 🔀 **Proxy Mode** - Forward requests to real backends
- Proxy-with-fallback (fallback to mock if upstream fails)
- Upstream configuration and timeouts

## File Structure

```
src/
├── core/              # FastAPI app, config, middleware, DI
├── domain/            # Business logic (entities, services, repositories)
├── infrastructure/    # Database, external services
├── application/       # DTOs, use cases, mappers
└── presentation/      # API endpoints

tests/
└── test_stage1_integration.py  # 10 passing tests
```

## Configuration

Settings are loaded from `.env` file or environment variables:

```env
MOCK_SERVER_HOST=0.0.0.0
MOCK_SERVER_PORT=18000
CONFIG_DATABASE_URL=sqlite+aiosqlite:///./mimicus.db
MOCK_LOG_LEVEL=INFO
```

## Development

### Code Quality

```bash
# Format code
black src/

# Lint
ruff check src/

# Type checking
mypy src/

# All together
black src/ && ruff check src/ && mypy src/
```

### Running Specific Tests

```bash
# Test health endpoint only
pytest tests/test_stage1_integration.py::TestHealthEndpoint -v

# Test mock matching only
pytest tests/test_stage1_integration.py::TestMockMatching -v

# With verbose output
pytest -v -s tests/test_stage1_integration.py
```

## Troubleshooting

### Port already in use
```bash
# Use a different port
export MOCK_SERVER_PORT=19000 && uv run python -m src.main
```

### Database errors
```bash
# Remove old database
rm mimicus.db

# Restart server (will create fresh database)
uv run python -m src.main
```

### Import errors
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
uv sync
```

## API Endpoints (Stage 1)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /health | Health check |
| GET | /ready | Readiness check |
| * | /{full_path} | Mock handler (any path/method) |

## Next Steps

1. **Start the server**: `uv run python -m src.main`
2. **Create mocks**: Use the code example above
3. **Test mocks**: `curl http://localhost:18000/...`
4. **Run tests**: `pytest tests/`
5. **Wait for Stage 2**: Template engine coming soon!

---

**Status**: Stage 1 Complete ✅
**Version**: 0.1.0
**Last Updated**: 2026-01-04
