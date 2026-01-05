# Matching Requests - Advanced Patterns

So far you've matched on method and path. Now let's match on headers, query parameters, and request bodies!

---

## The Matching Hierarchy

Mimicus matches mocks in this order:

```
1. HTTP Method (GET, POST, etc.)       ← Must match
2. URL Path (/api/users/1)             ← Must match
3. Headers (Authorization, etc.)       ← Optional, more specific
4. Query Parameters (?status=active)   ← Optional, more specific
5. Request Body ({"id": 1})            ← Optional, most specific

If ALL specified criteria match → Use this mock
```

---

## Basic Matching (Review)

### Method Matching

```json
{
  "match_method": "GET"
}
```

Only matches GET requests. POST, PUT, DELETE won't match.

### Path Matching

```json
{
  "match_path": "/api/users/1"
}
```

Only matches exact path. `/api/users/2` or `/api/users/1/profile` won't match.

---

## Advanced: Header Matching

### Match Specific Headers

```json
{
  "mock_name": "Get User (Authorized)",
  "match_method": "GET",
  "match_path": "/api/users/1",
  "match_headers": {
    "Authorization": "Bearer valid-token"
  },
  "response_status": 200,
  "response_body": "{\"id\": 1, \"name\": \"John\"}"
}
```

This mock **only** responds if the request includes:
```
Authorization: Bearer valid-token
```

### Multiple Header Conditions

```json
{
  "mock_name": "Get Admin Data",
  "match_method": "GET",
  "match_path": "/api/admin",
  "match_headers": {
    "Authorization": "Bearer admin-token",
    "X-Admin-Key": "secret123",
    "Accept": "application/json"
  },
  "response_status": 200,
  "response_body": "{\"data\": \"admin-only\"}"
}
```

All headers must match (AND logic):
- ✅ Request has all 3 headers → Match
- ❌ Request missing any header → No match

### Common Header Matching Scenarios

**Unauthorized Request:**

```json
{
  "mock_name": "API Requires Auth",
  "match_method": "GET",
  "match_path": "/api/secure",
  "match_headers": {
    "Authorization": "WRONG"
  },
  "response_status": 401,
  "response_body": "{\"error\": \"Unauthorized\"}"
}
```

**Browser vs API Client:**

```json
{
  "mock_name": "Desktop Browser",
  "match_headers": {
    "User-Agent": "Mozilla/5.0"
  },
  "response_body": "{\"format\": \"html\"}"
}
```

**Content Negotiation:**

```json
{
  "mock_name": "Get Data as XML",
  "match_headers": {
    "Accept": "application/xml"
  },
  "response_body": "<data>xml</data>",
  "response_headers": {
    "Content-Type": "application/xml"
  }
}
```

---

## Advanced: Query Parameter Matching

### Match Query Parameters

Query parameters are the `?key=value` part of URLs:

```
GET /api/users?status=active&limit=10
     ↑ Path       ↑ Query parameters
```

```json
{
  "mock_name": "Get Active Users Only",
  "match_method": "GET",
  "match_path": "/api/users",
  "match_query": {
    "status": "active"
  },
  "response_status": 200,
  "response_body": "[{\"id\": 1, \"status\": \"active\"}]"
}
```

**Request that matches:**
```
GET /api/users?status=active
```

**Requests that don't match:**
```
GET /api/users                    (no query param)
GET /api/users?status=inactive    (wrong status)
GET /api/users?limit=10           (different param)
```

### Multiple Query Parameters

```json
{
  "mock_name": "Filter Products",
  "match_method": "GET",
  "match_path": "/api/products",
  "match_query": {
    "category": "electronics",
    "sort": "price_asc",
    "limit": "20"
  },
  "response_body": "[{\"name\": \"Laptop\", \"price\": 999}]"
}
```

All query parameters must match:
```
GET /api/products?category=electronics&sort=price_asc&limit=20  ✅ Match

GET /api/products?category=electronics&sort=price_asc           ❌ No match (missing limit)

GET /api/products?category=electronics&sort=price_asc&limit=50  ❌ No match (wrong limit)
```

### Common Query Parameter Scenarios

**Pagination:**

```json
{
  "mock_name": "Get Page 2",
  "match_query": {
    "page": "2",
    "size": "10"
  },
  "response_body": "{\"items\": [...], \"page\": 2, \"total\": 100}"
}
```

**Search:**

```json
{
  "mock_name": "Search Products",
  "match_query": {
    "q": "laptop"
  },
  "response_body": "[{\"id\": 1, \"name\": \"Gaming Laptop\"}]"
}
```

**Filters:**

```json
{
  "mock_name": "Filter by Date Range",
  "match_query": {
    "from": "2024-01-01",
    "to": "2024-01-31"
  },
  "response_body": "{\"orders\": [...]}"
}
```

---

## Advanced: Request Body Matching

### Match Request Body Content

POST/PUT requests have a body. Match based on that body:

```json
{
  "mock_name": "Create User (Email Exists)",
  "match_method": "POST",
  "match_path": "/api/users",
  "match_body": {
    "email": "duplicate@example.com"
  },
  "response_status": 409,
  "response_body": "{\"error\": \"Email already exists\"}"
}
```

When request body contains:
```json
{"email": "duplicate@example.com", "name": "John"}
```

The mock matches! ✅

### Complex Body Matching

```json
{
  "mock_name": "Create Admin User",
  "match_method": "POST",
  "match_path": "/api/users",
  "match_body": {
    "email": "admin@example.com",
    "role": "admin"
  },
  "response_status": 201,
  "response_body": "{\"id\": 1, \"role\": \"admin\"}"
}
```

Requires both conditions:
- Email must be "admin@example.com"
- Role must be "admin"

### Common Body Matching Scenarios

**Conditional Creation:**

```json
{
  "mock_name": "Create Premium User",
  "match_method": "POST",
  "match_path": "/api/users",
  "match_body": {
    "plan": "premium"
  },
  "response_body": "{\"id\": 1, \"plan\": \"premium\", \"price\": 99}"
}
```

**Payment Processing:**

```json
{
  "mock_name": "Process Credit Card",
  "match_method": "POST",
  "match_path": "/api/payments",
  "match_body": {
    "method": "credit_card"
  },
  "response_body": "{\"status\": \"success\", \"transaction_id\": \"123\"}"
}
```

---

## Combining Multiple Conditions

### Match Headers AND Path

```json
{
  "mock_name": "Admin Only Endpoint",
  "match_method": "GET",
  "match_path": "/api/admin/users",
  "match_headers": {
    "X-Admin-Token": "secret123"
  },
  "response_body": "{\"users\": [...]}"
}
```

Requires:
- ✅ Path: `/api/admin/users`
- ✅ Header: `X-Admin-Token: secret123`

### Match Path, Query, AND Headers

```json
{
  "mock_name": "Complex Scenario",
  "match_method": "GET",
  "match_path": "/api/data",
  "match_query": {
    "type": "premium"
  },
  "match_headers": {
    "Authorization": "Bearer token"
  },
  "response_body": "{\"premium_data\": [...]}"
}
```

Requires **all** of:
- GET request
- Path: `/api/data`
- Query: `?type=premium`
- Header: `Authorization: Bearer token`

### Match Path, Query, AND Body

```json
{
  "mock_name": "Complex POST",
  "match_method": "POST",
  "match_path": "/api/transfer",
  "match_query": {
    "dry_run": "false"
  },
  "match_body": {
    "amount": "1000"
  },
  "response_body": "{\"status\": \"transferred\"}"
}
```

Requires **all** of:
- POST request
- Path: `/api/transfer`
- Query: `?dry_run=false`
- Body contains: `"amount": "1000"`

---

## Priority and Specificity

When multiple mocks match, what wins?

```
1. Most specific conditions → Higher priority
2. If tied → Use priority field (higher number wins)
```

### Example: Path Specificity

```json
// Mock 1: Matches any /api/users/*
{
  "mock_name": "Generic User",
  "match_path": "/api/users",
  "priority": 1
}

// Mock 2: Matches /api/users/1 with auth
{
  "mock_name": "Specific User with Auth",
  "match_path": "/api/users/1",
  "match_headers": {"Authorization": "Bearer token"},
  "priority": 100
}

// Request: GET /api/users/1 with Authorization header
// → Mock 2 wins (more specific)
```

### Example: Priority Tiebreaker

```json
// Mock 1: Matches /api/users
{
  "mock_name": "Standard Response",
  "match_path": "/api/users",
  "priority": 10
}

// Mock 2: Also matches /api/users
{
  "mock_name": "Special Response",
  "match_path": "/api/users",
  "priority": 50  // Higher priority wins
}

// Request: GET /api/users
// → Mock 2 wins (higher priority)
```

---

## Testing Matching

### Use Swagger UI

1. Visit `http://localhost:18000/docs`
2. Try your request with different headers/query params
3. See which mock responds

### Use curl with Headers

```bash
# Without header
curl http://localhost:18000/api/data
# Response: Mock 1

# With header
curl -H "Authorization: Bearer token" \
  http://localhost:18000/api/data
# Response: Mock 2 (header matched)
```

### Use curl with Query Parameters

```bash
# Without query
curl http://localhost:18000/api/users
# Response: Mock 1

# With query
curl "http://localhost:18000/api/users?status=active"
# Response: Mock 2 (query matched)
```

### Use curl with Body

```bash
# Send POST with body
curl -X POST http://localhost:18000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
# Response: Matching mock
```

---

## Common Matching Patterns

### Pattern 1: Version API

```json
{
  "mock_name": "API v1",
  "match_headers": {
    "Accept": "application/vnd.api+json;version=1"
  },
  "response_body": "{\"version\": 1, \"data\": \"v1\"}"
}
```

### Pattern 2: Locale-Based

```json
{
  "mock_name": "Spanish Response",
  "match_headers": {
    "Accept-Language": "es"
  },
  "response_body": "{\"mensaje\": \"Hola\"}"
}
```

### Pattern 3: Rate Limiting Bypass

```json
{
  "mock_name": "High Rate Limit",
  "match_headers": {
    "X-Rate-Limit-Bypass": "VIP123"
  },
  "response_headers": {
    "X-RateLimit-Limit": "10000"
  }
}
```

### Pattern 4: Feature Flags

```json
{
  "mock_name": "New Feature Enabled",
  "match_query": {
    "feature_flag": "new_checkout"
  },
  "response_body": "{\"checkout_enabled\": true}"
}
```

---

## Troubleshooting

### "My mock isn't matching"

Check in order:
1. ✅ HTTP method matches?
2. ✅ Path matches exactly?
3. ✅ All headers specified in mock are in request?
4. ✅ All query params specified in mock are in request?
5. ✅ All body fields specified in mock are in request?

### "Multiple mocks match, wrong one responding"

1. Check priorities (higher wins)
2. Make one more specific
3. Add distinguishing header/query/body

### "Escaping issues with special characters"

Use online JSON escape tool or:
```bash
# curl will handle escaping
curl -H 'X-Custom: value with spaces'  http://localhost:18000/api/data
```

---

## Next Steps

- 📝 **[Response Templates](response-templates.md)** - Dynamic responses based on request
- 🌐 **[Proxy Modes](proxy-modes.md)** - Forward unmatched requests
- 📤 **[Bulk Import](bulk-import.md)** - Create many mocks at once

---

**You can now match any request pattern!** 🎯
