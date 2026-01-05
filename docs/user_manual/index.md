# Welcome to Mimicus

## Mock Any API in Minutes ⚡

Mimicus is a universal HTTP mock and mimic service designed to help frontend developers and integration teams build and test their applications **without waiting for real backend APIs**.

Think of it as a flexible mock server that speaks the same language as your API. You define what endpoints you want, how they should respond, and Mimicus handles the rest—in seconds, not weeks.

### Perfect For

✅ **Frontend Teams** - Start building UI before APIs are ready
✅ **Integration Testing** - Test edge cases and error scenarios
✅ **API Development** - Mock endpoints while backend team is building
✅ **Performance Testing** - Simulate slow networks and delays
✅ **Team Collaboration** - Share mock definitions with your team via JSON files

### Key Features

🎯 **Define Mocks Instantly** - No Python required. Simple JSON definitions
🔄 **Dynamic Templating** - Generate realistic responses with Jinja2
📷 **Image Mocking** - Generate placeholder images or serve your own
🌐 **Proxy Mode** - Fall back to real APIs when available
🚀 **REST Admin API** - Manage mocks programmatically
📊 **Swagger UI** - Explore all your mocks visually

---

## Get Started in 5 Minutes

### 1. Install & Run
```bash
# Clone the repository
git clone https://github.com/your-org/mimicus.git
cd mimicus

# Install dependencies
uv sync

# Start the server
python main.py
```

The server starts on `http://localhost:18000/`

### 2. Create Your First Mock

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Get User",
    "match_method": "GET",
    "match_path": "/api/user/1",
    "response_status": 200,
    "response_body": "{\"id\": 1, \"name\": \"John Doe\", \"email\": \"john@example.com\"}"
  }'
```

### 3. Test It

```bash
curl http://localhost:18000/api/user/1
# Returns: {"id": 1, "name": "John Doe", "email": "john@example.com"}
```

**That's it!** You just created your first mock API.

---

## Why Mimicus?

### ⏱️ **Faster Development**
Stop waiting for backend teams. Mock the APIs you need right now.

### 🎨 **Zero Frontend Changes**
Seamlessly switch from mocks to real APIs—your frontend code stays the same.

### 📝 **Simple JSON Format**
No Python knowledge required. Define mocks using simple JSON files.

### 🔧 **Flexible & Powerful**
Generate dynamic responses, match complex request patterns, add delays, and more.

### 🤝 **Team Friendly**
Share mock definitions as files. Version control them with your code.

### 🏦 **Production Ready**
Used by teams at companies that care about quality frontend development.

---

## What You Can Build

### E-Commerce Store
Generate product mocks, test checkout flows, simulate payment scenarios—all before the backend exists.

### User Authentication
Mock login/logout flows, test error states, simulate token expiration.

### Real-Time Features
Simulate WebSocket connections, test polling, handle network errors gracefully.

### Complex Workflows
Build multi-step flows (wizard patterns, form validation, conditional rendering) with state management.

---

## Quick Navigation

- 🚀 **[Quick Start](getting-started/quick-start.md)** - 5 minutes to your first API mock
- 📚 **[Installation Guide](getting-started/installation.md)** - Detailed setup instructions
- 🎯 **[First Mock](getting-started/first-mock.md)** - Step-by-step tutorial
- 🤔 **[What is Mimicus?](concepts/what-is-mimicus.md)** - Understand the basics
- 📖 **[API Reference](api-reference/admin-api.md)** - All endpoints documented
- ⚛️ **[React Integration](frontend-integration/react-setup.md)** - Hook up to your frontend
- 🖼️ **[Image Mocking](image-mocking/overview.md)** - Generate or serve images
- 🏪 **[E-Commerce Tutorial](tutorials/ecommerce-store.md)** - Build a complete store mock

---

## Still Have Questions?

- 🔍 Check the [Troubleshooting Guide](getting-started/troubleshooting.md)
- 📖 Browse the [Full Documentation](#)
- 💬 Open an issue on GitHub
- 🐛 Read the [Glossary](reference/glossary.md) for common terms

---

## Next Steps

Ready to get started? Head to the **[Quick Start Guide](getting-started/quick-start.md)** →

Or, if you prefer learning by concepts, start with **[What is Mimicus?](concepts/what-is-mimicus.md)** →
