# Creating Mocks - Complete Guide

Let's dive deep into creating mocks. You already know the basics—now let's master it!

---

## The Anatomy of a Mock

Every mock has these key parts:

```json
{
  "mock_name": "Friendly name for this mock",
  "match_method": "HTTP method (GET, POST, etc.)",
  "match_path": "URL path to match",
  "response_status": 200,
  "response_body": "JSON response as a string",
  "response_headers": {"optional": "headers"},
  "response_delay_ms": 0,
  "enabled": true,
  "priority": 100
}
```

Let's break down each part.

---

## 1. mock_name - What to Call It

**Purpose:** Friendly identifier for your mock

**Format:** Use descriptive names

```json
{
  "mock_name": "Get User by ID"      // ✅ Good
  "mock_name": "user-get"            // ✅ Okay
  "mock_name": "endpoint"            // ❌ Too vague
  "mock_name": "mock1"               // ❌ Not descriptive
}
```

**Tips:**
- Include the action (Get, Create, Update, Delete)
- Include what you're getting (User, Product, Order)
- Include special conditions if needed (Get User by ID, Get User with Admin Role)

---

## 2. match_method - Which HTTP Method

**Purpose:** Match specific HTTP methods

**Valid values:**
```json
{
  "match_method": "GET"      // Retrieve data
  "match_method": "POST"     // Create data
  "match_method": "PUT"      // Replace data
  "match_method": "PATCH"    // Partial update
  "match_method": "DELETE"   // Remove data
  "match_method": "HEAD"     // Like GET, no body
  "match_method": "OPTIONS"  // Describe communication
}
```

**Examples:**

```json
// Get a resource
{
  "mock_name": "Fetch Product",
  "match_method": "GET",
  "match_path": "/api/products/1"
}

// Create a resource
{
  "mock_name": "Create Order",
  "match_method": "POST",
  "match_path": "/api/orders"
}

// Update a resource
{
  "mock_name": "Update User",
  "match_method": "PUT",
  "match_path": "/api/users/1"
}

// Delete a resource
{
  "mock_name": "Cancel Subscription",
  "match_method": "DELETE",
  "match_path": "/api/subscriptions/1"
}
```

---

## 3. match_path - Which URL Path

**Purpose:** Match requests to specific paths

**Format:** Absolute path (starts with `/`)

```json
{
  "match_path": "/api/products/1"      // ✅ Exact path
  "match_path": "/api/products"        // ✅ Collection path
  "match_path": "/products/1"          // ✅ Without /api prefix
  "match_path": "api/products"         // ❌ Missing leading /
  "match_path": "http://api.com/path"  // ❌ Don't include domain
}
```

**Path Matching Rules:**

Exact match:
```json
Mock path: "/api/users/1"
Request:   "/api/users/1"     → MATCH ✅
Request:   "/api/users/2"     → NO MATCH ❌
Request:   "/api/users"       → NO MATCH ❌
Request:   "/api/users/1/bio" → NO MATCH ❌
```

---

## 4. response_status - HTTP Status Code

**Purpose:** Return specific HTTP status codes

**Common codes:**

```json
{
  "response_status": 200     // Success - resource found
  "response_status": 201     // Created - new resource created
  "response_status": 204     // No Content - success but no body
  "response_status": 400     // Bad Request - invalid input
  "response_status": 401     // Unauthorized - need login
  "response_status": 403     // Forbidden - no permission
  "response_status": 404     // Not Found - resource missing
  "response_status": 409     // Conflict - duplicate, etc.
  "response_status": 500     // Server Error - something broke
  "response_status": 503     // Service Unavailable - down
}
```

**Examples:**

```json
// Success
{
  "mock_name": "Fetch User",
  "match_method": "GET",
  "match_path": "/api/users/1",
  "response_status": 200,
  "response_body": "{\"id\": 1, \"name\": \"John\"}"
}

// User not found
{
  "mock_name": "Fetch User (Not Found)",
  "match_method": "GET",
  "match_path": "/api/users/999",
  "response_status": 404,
  "response_body": "{\"error\": \"User not found\"}"
}

// Unauthorized
{
  "mock_name": "Fetch Admin (Unauthorized)",
  "match_method": "GET",
  "match_path": "/api/admin/panel",
  "response_status": 401,
  "response_body": "{\"error\": \"Authentication required\"}"
}

// Server error
{
  "mock_name": "Database Error",
  "match_method": "GET",
  "match_path": "/api/data",
  "response_status": 500,
  "response_body": "{\"error\": \"Database connection failed\"}"
}
```

---

## 5. response_body - The Response Data

**Purpose:** Define what data to return

**Important:** Must be a **JSON string**, not a JSON object

```json
// ❌ WRONG - JSON object
"response_body": {"id": 1, "name": "John"}

// ✅ RIGHT - JSON string with escaped quotes
"response_body": "{\"id\": 1, \"name\": \"John\"}"
```

**How to escape JSON:**

1. Take your JSON:
```json
{"id": 1, "name": "John", "email": "john@example.com"}
```

2. Escape the quotes:
```json
"{\"id\": 1, \"name\": \"John\", \"email\": \"john@example.com\"}"
```

3. Use in response_body:
```json
{
  "mock_name": "Get User",
  "response_body": "{\"id\": 1, \"name\": \"John\", \"email\": \"john@example.com\"}"
}
```

**Using an online tool:**
- Use [JSONFormatter.org](https://jsonformatter.org/json-escape) to escape quotes automatically

**Complex Example:**

```json
{
  "mock_name": "Get Product with Details",
  "response_body": "{\"id\": 1, \"name\": \"Laptop\", \"price\": 999.99, \"specs\": {\"cpu\": \"Intel i7\", \"ram\": \"16GB\"}, \"reviews\": [{\"rating\": 5, \"text\": \"Great!\"}]}"
}
```

---

## 6. response_headers - Custom Headers

**Purpose:** Add custom headers to responses

```json
{
  "response_headers": {
    "Content-Type": "application/json",
    "Cache-Control": "max-age=3600",
    "X-Custom-Header": "my-value"
  }
}
```

**Common Headers:**

```json
{
  "response_headers": {
    "Content-Type": "application/json",       // Data format
    "Cache-Control": "max-age=3600",          // Cache for 1 hour
    "X-RateLimit-Limit": "100",               // Rate limit
    "X-RateLimit-Remaining": "99",            // Calls remaining
    "Access-Control-Allow-Origin": "*",       // CORS
    "Authorization": "Bearer token"           // Auth token
  }
}
```

**Example:**

```json
{
  "mock_name": "Get User",
  "match_method": "GET",
  "match_path": "/api/users/1",
  "response_status": 200,
  "response_body": "{\"id\": 1, \"name\": \"John\"}",
  "response_headers": {
    "Cache-Control": "public, max-age=3600",
    "X-Response-Time": "12ms"
  }
}
```

---

## 7. response_delay_ms - Simulate Latency

**Purpose:** Simulate network delay

```json
{
  "response_delay_ms": 0        // Instant (default)
  "response_delay_ms": 500      // Half second
  "response_delay_ms": 2000     // 2 seconds
  "response_delay_ms": 5000     // 5 seconds
}
```

**Use cases:**

Test loading spinners:
```json
{
  "mock_name": "Slow API",
  "response_delay_ms": 3000,
  "response_body": "{\"data\": \"...\"}"
}
```

Your code shows spinner for 3 seconds before data appears.

Test timeout handling:
```json
{
  "mock_name": "Very Slow API",
  "response_delay_ms": 30000,    // 30 seconds
  "response_body": "{\"data\": \"...\"}"
}
```

Your code times out (usually after 10-15 seconds).

---

## 8. enabled - Enable/Disable

**Purpose:** Turn mocks on or off without deleting

```json
{
  "enabled": true    // Mock is active
  "enabled": false   // Mock is disabled (404 if requested)
}
```

**Use case:**

Test switching between mocks:
```json
// Mock 1 - Fast response
{
  "mock_name": "Get User (Fast)",
  "enabled": false,  // Disabled
  "response_delay_ms": 100
}

// Mock 2 - Slow response
{
  "mock_name": "Get User (Slow)",
  "enabled": true,   // Active
  "response_delay_ms": 3000
}
```

---

## 9. priority - Which Mock Wins

**Purpose:** When multiple mocks match, priority decides

**Rules:**
- Higher number = higher priority
- Default: 100
- Range: 0-1000

```json
Mock 1: priority: 10    (low)
Mock 2: priority: 100   (medium)
Mock 3: priority: 500   (high) ← Used

Request matches all 3 → Mock 3's response is returned
```

**Example:**

```json
// General mock - low priority
{
  "mock_name": "Get User",
  "match_path": "/api/users/1",
  "priority": 10,
  "response_body": "{\"name\": \"John\"}"
}

// Special case - high priority
{
  "mock_name": "Get User (Admin Override)",
  "match_path": "/api/users/1",
  "priority": 100,
  "response_body": "{\"name\": \"John\", \"role\": \"admin\"}"
}

Request to /api/users/1 → Gets Admin response
```

---

## Complete Examples

### Example 1: Simple GET

```json
{
  "mock_name": "Fetch Product",
  "match_method": "GET",
  "match_path": "/api/products/1",
  "response_status": 200,
  "response_body": "{\"id\": 1, \"name\": \"Wireless Headphones\", \"price\": 79.99, \"in_stock\": true}"
}
```

### Example 2: POST with Error

```json
{
  "mock_name": "Create User (Email Already Exists)",
  "match_method": "POST",
  "match_path": "/api/users",
  "response_status": 409,
  "response_body": "{\"error\": \"Email already exists\", \"field\": \"email\"}"
}
```

### Example 3: Slow Response with Headers

```json
{
  "mock_name": "Get User with Caching",
  "match_method": "GET",
  "match_path": "/api/users/1",
  "response_status": 200,
  "response_body": "{\"id\": 1, \"name\": \"Alice\", \"email\": \"alice@example.com\"}",
  "response_headers": {
    "Cache-Control": "public, max-age=3600",
    "ETag": "123abc"
  },
  "response_delay_ms": 500
}
```

### Example 4: Server Error

```json
{
  "mock_name": "Database Connection Error",
  "match_method": "GET",
  "match_path": "/api/data",
  "response_status": 500,
  "response_body": "{\"error\": \"Internal Server Error\", \"details\": \"Database timeout\"}"
}
```

---

## Creating via API

### Using curl

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Get User",
    "match_method": "GET",
    "match_path": "/api/users/1",
    "response_status": 200,
    "response_body": "{\"id\": 1, \"name\": \"John\"}"
  }'
```

### Using Postman

1. Create POST request to `http://localhost:18000/api/admin/mocks`
2. Set Body → JSON
3. Paste mock definition
4. Click Send

### Using Swagger UI

1. Visit `http://localhost:18000/docs`
2. Find "POST /api/admin/mocks"
3. Click "Try it out"
4. Paste mock definition
5. Click "Execute"

---

## Best Practices

### ✅ Do

- Use clear, descriptive names
- Test all HTTP methods (GET, POST, PUT, DELETE)
- Include error scenarios (404, 500, etc.)
- Document your mocks in a file or database
- Use priorities for overlapping paths
- Start simple, add complexity as needed

### ❌ Don't

- Use vague names (like "test" or "api")
- Forget to escape JSON quotes
- Ignore error status codes
- Hardcode user IDs if they're variables
- Create too many similar mocks
- Leave mocks disabled accidentally

---

## Next Steps

- 🔍 **[Matching Requests](matching-requests.md)** - Match on headers, query params, body
- 📝 **[Response Templates](response-templates.md)** - Make dynamic responses
- 🌐 **[Proxy Modes](proxy-modes.md)** - Fall back to real backend
- 📤 **[Bulk Import](bulk-import.md)** - Import from files

---

**You're ready to create amazing mocks!** 🚀
