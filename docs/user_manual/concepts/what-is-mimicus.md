# What is Mimicus?

Mimicus is a **mock HTTP server**—think of it as a stunt double for your real API.

## Simple Definition

Mimicus lets you create fake API endpoints that respond exactly like your real backend would, **without needing the real backend to exist**.

```
Your Frontend → Mimicus (fake API) → Returns mock data
Your Frontend → Real Backend → Returns real data

^^ The frontend can't tell the difference!
```

## Why Would You Want This?

### Scenario 1: Real API Isn't Ready Yet
Your frontend team is ready to build, but the backend team needs another 2 weeks to finish the API.

**Without Mimicus:** Frontend developers sit idle waiting.
**With Mimicus:** Frontend developers mock the API in 5 minutes and start building immediately.

### Scenario 2: Testing Edge Cases
You want to test what happens when the API returns an error (500 Server Error, 404 Not Found, etc.), but the real API almost never does.

**Without Mimicus:** Hope for a bug to test error handling (dangerous!).
**With Mimicus:** Create a mock that returns errors on demand.

### Scenario 3: No Backend Needed
You're building a static website, landing page, or simple UI demo where you don't actually need a real backend.

**Without Mimicus:** Still have to set up backend infrastructure.
**With Mimicus:** Just use Mimicus—that's it.

---

## How Mimicus Works (Simple Version)

```
1. You Define → What requests should match?
                How should they respond?

2. Mimicus Runs → Listens for incoming requests

3. When a Request Arrives → Does it match a defined mock?
                            ↓
                      YES → Return the mocked response
                      NO  → Return 404 (not found)
```

## Example

You define this mock:
```json
{
  "mock_name": "Get User",
  "match_method": "GET",
  "match_path": "/api/users/1",
  "response_body": "{\"id\": 1, \"name\": \"Alice\", \"email\": \"alice@example.com\"}"
}
```

Then:
```bash
# Your code requests this
GET /api/users/1

# Mimicus finds a matching mock
# Returns this
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

Your code doesn't know it's a mock—it just looks like a normal API response!

---

## Key Features

### 🎯 Instant Mocks
Define a new endpoint in seconds with simple JSON.

### 📝 Dynamic Responses
Generate different responses based on what the request contains (using Jinja2 templates).

### 🔄 Request Matching
Match requests based on:
- HTTP method (GET, POST, etc.)
- URL path
- Headers
- Query parameters
- Request body

### 🖼️ Image Mocking
Need placeholder images? Generate them on the fly with custom dimensions.

### 🌐 Proxy Mode
Can't mock everything? Fall back to your real backend for unmocked endpoints.

### 🛡️ Error Simulation
Test how your app handles errors—return any HTTP status code you want.

### 📊 Admin API
Manage your mocks programmatically via REST API.

### 🔍 Swagger UI
Explore all your mock endpoints in an interactive web interface.

---

## What Mimicus Is NOT

### ❌ A Database
Mimicus doesn't store data persistently by default. Data is in-memory and resets when you restart the server.

### ❌ A Full Backend
If you need complex business logic, complex database queries, or authentication, you'll eventually need a real backend.

### ❌ For Production
Mimicus is for development and testing. Don't use it to mock real users' traffic.

### ❌ Automatic
It doesn't magically know what your backend should do. You have to tell it.

---

## Who Should Use Mimicus?

✅ **Frontend developers** - Start building before backend is ready
✅ **QA engineers** - Test edge cases and error scenarios
✅ **Product managers** - Demo features without real backend
✅ **Integration teams** - Test API integrations before connecting to production
✅ **Full-stack developers** - Mock APIs while building different services

---

## Mimicus vs Other Tools

| Feature | Mimicus | Postman Mock | json-server | Real Backend |
|---------|---------|--------------|-------------|--------------|
| Setup Time | 30 seconds | 2 minutes | 5 minutes | Hours/Days |
| No Code Needed | ✅ | ✅ | ❌ | ❌ |
| Dynamic Responses | ✅ | ✅ | ✅ | ✅ |
| Image Generation | ✅ | ❌ | ❌ | ✅ |
| Full Backend Logic | ❌ | ❌ | ❌ | ✅ |
| Free & Open Source | ✅ | ❌ | ✅ | Varies |

---

## The Mimicus Workflow

```
1. START → Team needs API, but backend isn't ready

2. DESIGN → Write mock definitions in JSON
           Define request patterns and responses

3. CREATE → Upload mocks to Mimicus using admin API
           Or import from OpenAPI spec

4. DEVELOP → Frontend team builds with mocks
            No waiting for real backend

5. TEST → Test all scenarios:
          - Success cases
          - Error cases
          - Edge cases

6. SWITCH → When real backend is ready:
            Change one environment variable
            Frontend code stays the same!

7. DONE → Ship with confidence
```

---

## Next Steps

Ready to dive deeper?

- 🤔 **[Why Use Mocks?](why-use-mocks.md)** - More reasons to use Mimicus
- 🔧 **[How It Works](how-it-works.md)** - More technical details
- 📊 **[Mock vs Real API](mock-vs-real-api.md)** - Comparison and best practices
- 🚀 **[Quick Start](../getting-started/quick-start.md)** - Start building!

---

## Summary

**Mimicus is your fake API server.** It lets you build and test your frontend without waiting for a real backend. Create mocks in seconds, test everything, and when your real backend is ready, just switch the URL—your code doesn't change.

That's powerful! 🚀
