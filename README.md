# 🎭 Mimicus

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/hr1juldey/mimicus/releases)
[![Python](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.110+-blueviolet.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/hr1juldey/mimicus)

> **Universal Mock & Mimic Service** — Mock any HTTP API in seconds. Zero backend needed.

The ultimate mock server for frontend developers, integration teams, and QA engineers. Build, test, and ship **without waiting for real APIs**.

## ✨ What You Can Do

### 🚀 **Mock Any API**

- Define realistic mock APIs with flexible request matching
- Generate dynamic responses using Jinja2 templates
- Match on method, path, headers, query params, and body
- Control response with priority rules

### 🎨 **Generate Images On-the-Fly**

- Placeholder images with custom dimensions (1-8000px)
- Device presets (mobile, tablet, desktop)
- Upload your own images with auto-detection
- Perfect for responsive design testing

### 🔄 **Seamless Switching**

- Start with mocks, switch to real API without code changes
- Proxy mode with fallback to mocks
- Import OpenAPI specs to auto-generate mocks

### ⚡ **Test Everything**

- Simulate errors (404, 500, timeouts)
- Add realistic delays
- Test edge cases before backend exists
- Load test with controlled responses

**Perfect for:**

- ✅ Frontend teams waiting for backend
- ✅ Integration testing with multiple API versions
- ✅ Development environment isolation
- ✅ API contract testing
- ✅ Responsive design testing across devices
- ✅ QA edge case simulation

---

## 🚀 Quick Start in 5 Minutes

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/hr1juldey/mimicus.git
cd mimicus

# Install dependencies
uv sync

# Start the server
python main.py
```

✅ **Server running!** Open: `http://localhost:18000`

### Create Your First Mock

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Get User",
    "match_method": "GET",
    "match_path": "/api/users/1",
    "response_status": 200,
    "response_body": "{\"id\": 1, \"name\": \"John\", \"email\": \"john@example.com\"}"
  }'
```

### Test Your Mock

```bash
curl http://localhost:18000/api/users/1
# Returns: {"id": 1, "name": "John", "email": "john@example.com"}
```

### 🎨 Generate Images On-the-Fly

```bash
# Generate a 300x200 placeholder image
curl http://localhost:18000/api/images/300x200 > image.png

# Get device presets (mobile, tablet, desktop)
curl http://localhost:18000/api/images/responsive/mobile

# Upload your own image
curl -X POST http://localhost:18000/api/images/upload -F "file=@product.jpg"
```

🎉 **That's it!** Your mock API is live with images.

---

## Architecture Overview

Mimicus follows a **clean, layered architecture** with clear separation of concerns:

```bash
┌──────────────────────────────────────────────────┐
│         Presentation Layer (FastAPI)             │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │
│  │  Admin   │  │  Mocks   │  │   Health     │    │
│  │   API    │  │  Handler │  │   Endpoint   │    │
│  └────┬─────┘  └────┬─────┘  └──────────────┘    │
└───────┼─────────────┼────────────────────────────┘
        │             │
   ┌────▼─────────────▼──────────────┐
   │   Application Layer              │
   │  ┌──────────────────────────┐    │
   │  │  Use Cases (Stage 5)     │    │
   │  │  DTOs & Mappers          │    │
   │  └──────────────────────────┘    │
   └────┬─────────────────────────────┘
        │
   ┌────▼──────────────────────────┐
   │   Domain Layer                │
   │  ┌──────────┐  ┌────────────┐ │
   │  │ Entities │  │  Services  │ │
   │  │  (Mock,  │  │ (Matching, │ │
   │  │  Match)  │  │ Response)  │ │
   │  └──────────┘  └────────────┘ │
   └────┬──────────────────────────┘
        │
   ┌────▼──────────────────────────┐
   │   Infrastructure Layer        │
   │  ┌──────────┐  ┌────────────┐ │
   │  │Database  │  │    HTTP    │ │
   │  │(SQLite)  │  │   Client   │ │
   │  └──────────┘  └────────────┘ │
   └───────────────────────────────┘
```

### Key Layers

**Presentation Layer:** FastAPI routes handling HTTP requests

- Admin API for CRUD operations on mock definitions
- Mock handler for dynamic request routing
- Health check endpoints

**Application Layer:** Business logic orchestration

- Use Cases: CreateMock, UpdateMock, DeleteMock, etc.
- DTOs: Data transfer between API and domain
- Mappers: Entity ↔ DTO conversions

**Domain Layer:** Core business logic

- Entities: MockDefinition with MatchCriteria & ResponseConfig
- Services: MatchingService, ResponseService, TemplateService, ProxyService
- Repositories: Abstract data access interface

**Infrastructure Layer:** External systems

- Database: SQLite with SQLModel ORM
- HTTP Client: Async proxy requests to upstream servers
- Configuration: Environment-based settings

---

## How to Use

### 1. Create a Mock

Create a simple mock via the admin API:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Get User",
    "match_method": "GET",
    "match_path": "/api/users/1",
    "response_status": 200,
    "response_headers": {"Content-Type": "application/json"},
    "response_body": "{\"id\": 1, \"name\": \"John Doe\", \"email\": \"john@example.com\"}",
    "mock_mode": "mock"
  }'
```

### 2. Access the Mock

Call the mocked endpoint:

```bash
curl http://localhost:18000/api/users/1
# Response: {"id": 1, "name": "John Doe", "email": "john@example.com"}
```

### 3. Use Dynamic Responses (Templates)

Create a mock with Jinja2 templating to echo back request data:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Echo User",
    "match_method": "POST",
    "match_path": "/api/users",
    "response_status": 201,
    "response_body": "{\"created\": true, \"name\": \"{{ request.json.name }}\", \"timestamp\": \"{{ now() }}\"}",
    "is_template": true,
    "mock_mode": "mock"
  }'
```

Template variables available:

- `{{ request.json }}` - Request body as dict
- `{{ request.headers }}` - Request headers
- `{{ request.query }}` - Query parameters
- `{{ now() }}` - Current timestamp
- `{{ random_token(16) }}` - Random string
- `{{ faker('name') }}` - Fake data generation

### 4. Proxy to Real Backend with Fallback

When your backend comes online, use proxy-with-fallback to try real API first:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Proxy Users API",
    "match_method": "GET",
    "match_path": "/api/users",
    "mock_mode": "proxy-with-fallback",
    "upstream_url": "https://api.myapp.com",
    "response_body": "{\"error\": \"Backend unavailable\", \"fallback\": true}",
    "timeout_seconds": 5
  }'
```

Modes:

- **mock** - Return static/template response
- **proxy** - Always forward to upstream (fail if unreachable)
- **proxy-with-fallback** - Try upstream, fallback to mock response on error
- **passthrough** - Forward to upstream, fail if unreachable

### 5. Match Requests by Multiple Criteria

Create mocks with flexible matching:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Admin Only",
    "match_method": "POST",
    "match_path": "/api/admin/users",
    "match_headers": {"Authorization": "Bearer admin-token"},
    "response_status": 200,
    "response_body": "{\"status\": \"admin access granted\"}",
    "mock_mode": "mock"
  }'
```

Matching criteria:

- **Method:** GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- **Path:** Exact or template patterns (e.g., `/users/{id}`)
- **Headers:** Match on specific header values
- **Query Parameters:** Match on specific query params

### 6. Priority-Based Selection

Multiple mocks can match the same request. Use priority to control which is selected:

```bash
# Higher priority = selected first
# Priority 200 is selected over priority 100
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Specific User 1",
    "match_method": "GET",
    "match_path": "/api/users/1",
    "mock_priority": 200,
    "response_body": "{\"id\": 1, \"name\": \"Special User\"}"
  }'
```

### 7. Simulate Delays

Add realistic response latency:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Slow API",
    "match_method": "GET",
    "match_path": "/api/slow",
    "response_delay_ms": 2000,
    "response_body": "{\"delayed\": true}",
    "mock_mode": "mock"
  }'
```

### 8. Manage Mocks

List all mocks:

```bash
curl http://localhost:18000/api/admin/mocks
```

Get a specific mock:

```bash
curl http://localhost:18000/api/admin/mocks/{mock_id}
```

Update a mock:

```bash
curl -X PUT http://localhost:18000/api/admin/mocks/{mock_id} \
  -H "Content-Type: application/json" \
  -d '{"response_body": "{\"updated\": true}"}'
```

Delete a mock:

```bash
curl -X DELETE http://localhost:18000/api/admin/mocks/{mock_id}
```

Toggle enabled status:

```bash
curl -X PATCH http://localhost:18000/api/admin/mocks/{mock_id}/toggle
```

---

## Configuration

Environment variables (`.env`):

```env
# Server
CONFIG_PORT=18000

# Database
CONFIG_DATABASE_URL=sqlite:///./mimicus.db

# Upstream proxy settings
CONFIG_PROXY_TIMEOUT=10
```

---

## Testing

Run the full test suite:

```bash
pytest              # Run all tests
pytest -v           # Verbose output
pytest --cov=src    # With coverage report
```

Current test coverage:

- **Stage 1:** Core Mock Engine (10 tests)
- **Stage 2:** Template Engine (15 tests)
- **Stage 3:** Admin REST API (17 tests)
- **Stage 4:** Proxy Mode (8 tests)
- **Total:** 50+ tests passing

---

## Development Roadmap

### ✅ Completed (Stages 1-5)

**Stage 1-4: Core Features**
- ✅ Core mock request matching and response generation
- ✅ Jinja2 template support with request variables
- ✅ Admin REST API for CRUD operations
- ✅ Proxy modes with upstream fallback
- ✅ Comprehensive test coverage (50+ tests)

**Stage 5: Image Generation & Documentation**
- ✅ Dynamic placeholder image generation (1-8000px)
- ✅ Device presets (mobile, tablet, desktop)
- ✅ User image upload with auto-dimension detection
- ✅ Responsive image set generation
- ✅ Image caching with file-based storage
- ✅ Complete User Manual (26 documentation files)
- ✅ MkDocs integration with Material theme
- ✅ GitHub Pages ready deployment
- ✅ Comprehensive API reference
- ✅ React integration guide

### 🔄 In Progress (Stage 6)

- 🔄 GitHub Actions auto-deployment workflow
- 🔄 Advanced testing frameworks
- 🔄 Performance optimization

### 🔜 Coming Soon (Stages 7-9)

- 🔜 **Stage 7:** JWT Authentication & API Keys
- 🔜 **Stage 8:** OpenAPI Spec Import & File Storage
- 🔜 **Stage 9:** Redis Caching Layer & Advanced Features

---

## Project Structure

```bash
mimicus/
├── src/
│   ├── core/                 # Application setup & configuration
│   │   ├── app.py
│   │   ├── config.py
│   │   └── dependencies.py
│   ├── domain/               # Business logic
│   │   ├── entities/
│   │   ├── services/
│   │   └── repositories/
│   ├── application/          # Use cases & DTOs
│   │   ├── use_cases/       # (Stage 5)
│   │   ├── dtos/
│   │   └── mappers/
│   ├── infrastructure/       # External integrations
│   │   └── external/
│   └── presentation/         # FastAPI routes
│       └── api/
├── tests/                    # Test suite (pytest)
├── docs/                     # Design documents
│   ├── HLD.md
│   ├── LLD.md
│   └── VARIABLE_NAMES.md
├── main.py                   # FastMCP entry point
├── pyproject.toml            # Project configuration
├── uv.lock                   # Dependency lock
└── CLAUDE.md                 # Developer guide
```

---

## Code Quality Standards

- **100 lines max per file** (enforces focused, maintainable modules)
- **SOLID principles:** SRP, OCP, LSP, ISP, DIP
- **Domain-Driven Design:** Entities, Services, Repositories, Use Cases
- **DRY:** No code duplication, reusable components
- **Async/Await:** Non-blocking I/O throughout
- **Type Safety:** Pydantic v2 for validation

---

## Contributing

1. Follow the code standards in `CLAUDE.md`
2. Write tests for new features
3. Ensure all tests pass: `pytest`
4. Use type annotations throughout
5. Keep files under 100 lines

---

## License

MIT

---

## 📖 Documentation & Support

- **Full User Manual:** [https://hr1juldey.github.io/mimicus/](https://hr1juldey.github.io/mimicus/)
- **Quick Start:** [Getting Started Guide](https://hr1juldey.github.io/mimicus/getting-started/)
- **API Reference:** [Complete Endpoint Docs](https://hr1juldey.github.io/mimicus/api-reference/image-api/)
- **Image Mocking:** [Guide & Examples](https://hr1juldey.github.io/mimicus/image-mocking/)
- **Design Docs:** See `docs/HLD.md` & `docs/LLD.md`
- **Developer Guide:** See `CLAUDE.md`

---

## 👤 Creator

### **Hrijul Dey**

📧 [Mail](mailto:deyinmylife5@gmail.com) | [LinkedIn](https://www.linkedin.com/in/dey-h-ml972/) | [𝕏](https://x.com/HrijulD)

---

**Built with FastAPI, Pillow, Jinja2, and async/await for modern Python development.**

**MIT License** — Free to use and modify
