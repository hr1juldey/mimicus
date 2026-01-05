# How It Works - Under the Hood

Let's look at how Mimicus actually works. Don't worry—it's simpler than it sounds!

---

## The Simple Version

```
1. Your Code Makes a Request
   GET /api/users/1

2. Mimicus Receives It
   ↓ "Do I have a mock for this?"

3. Mimicus Matches
   ↓ Found! "Get User" mock

4. Mimicus Responds
   Returns: {"id": 1, "name": "Alice", ...}

5. Your Code Gets Response
   Treats it like a real API response
   Works normally!
```

---

## Step 1: You Create Mocks

Before Mimicus can respond, you tell it what to respond with:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Get User",
    "match_method": "GET",
    "match_path": "/api/users/1",
    "response_status": 200,
    "response_body": "{\"id\": 1, \"name\": \"Alice\"}"
  }'
```

Mimicus stores this in memory (or database):

| Field | Value |
|-------|-------|
| name | Get User |
| match_method | GET |
| match_path | /api/users/1 |
| response_status | 200 |
| response_body | {"id": 1, "name": "Alice"} |
| enabled | true |

---

## Step 2: Request Comes In

Your code (or browser) makes a request:

```bash
curl -X GET http://localhost:18000/api/users/1
```

This becomes:

```
Method: GET
Path: /api/users/1
Headers: {Content-Type: application/json, ...}
Body: (empty for GET)
```

---

## Step 3: Mimicus Matches

Mimicus looks through all mocks asking: **"Does this match?"**

For each mock, it checks:

```
Does Method Match?
  GET == GET? ✅ YES

Does Path Match?
  /api/users/1 == /api/users/1? ✅ YES

Does Everything Match?
  ✅ YES → Found our mock!
```

If it finds multiple matches, it uses:
1. **Most specific path first** (exact > wildcard)
2. **Priority** (higher priority wins)

---

## Step 4: Mimicus Responds

Once matched, Mimicus returns the response:

```
Status: 200
Body: {"id": 1, "name": "Alice"}
Headers: Content-Type: application/json
```

This looks **exactly** like a real API response!

---

## Step 5: Your Code Never Knows

Your code receives the response normally:

```javascript
const response = await fetch('http://localhost:18000/api/users/1');
const user = await response.json();

console.log(user);  // {"id": 1, "name": "Alice"}
// ^ Your code thinks this came from a real API!
```

---

## Request Matching in Detail

Mocks can match on more than just method and path!

### Method Matching

```
Mock says: match_method = "POST"

Request 1: GET /api/users → No match
Request 2: POST /api/users → MATCH!
Request 3: PUT /api/users → No match
```

### Path Matching

```
Mock says: match_path = "/api/users/1"

Request 1: /api/users → No match
Request 2: /api/users/1 → MATCH!
Request 3: /api/users/1/profile → No match
```

### Advanced Matching (Optional)

You can also match on:

```json
{
  "match_method": "POST",
  "match_path": "/api/users",
  "match_headers": {"Authorization": "Bearer token123"},
  "match_query": {"filter": "active"},
  "match_body": {"name": "John"}
}
```

This mock only matches if **ALL** conditions are met.

---

## Response Generation

### Static Response (Simple)

```json
{
  "mock_name": "Get User",
  "response_body": "{\"id\": 1, \"name\": \"Alice\"}"
}
```

Every request gets the same response.

### Dynamic Response (Advanced)

```json
{
  "mock_name": "Get User",
  "response_body": "{\"id\": {{ request.path_params.user_id }}, \"name\": \"{{ request.query.name }}\"}"
}
```

Response changes based on the **request**!

If you request:
```
GET /api/users/1?name=Alice
```

Response becomes:
```json
{"id": 1, "name": "Alice"}
```

---

## Status Codes

Mimicus returns whatever status code you define:

```json
{
  "response_status": 200  // Success
}
```

Common codes:

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Need auth |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Something broke |

---

## Response Headers

Mimicus can add headers to responses:

```json
{
  "response_status": 200,
  "response_headers": {
    "Content-Type": "application/json",
    "Cache-Control": "max-age=3600"
  }
}
```

---

## Priority and Fallback

What if multiple mocks match the same request?

```
Mock 1: match_path = "/api/users/1"    priority = 10
Mock 2: match_path = "/api/users/*"    priority = 1

Request: GET /api/users/1

✅ Both match, but Mock 1 has higher priority
→ Return Mock 1's response
```

If **no** mocks match:
```
Request: GET /api/endpoint-that-doesnt-exist

❌ No mocks match
→ Return 404 Not Found
```

You can also set a **fallback** to your real backend:

```json
{
  "proxy_to_upstream": "https://real-api.example.com"
}
```

If no mock matches, forward to real backend!

---

## State (Advanced)

Mocks can maintain state:

```json
{
  "mock_name": "Create User",
  "match_method": "POST",
  "match_path": "/api/users",
  "response_body": "{\"id\": 3, \"name\": \"{{ request.body.name }}\"}",
  "state_persist_to": "user_list"
}
```

When this mock is called, it updates state:
- Increment user ID
- Add user to list
- Return new user ID

Later requests can use this state!

---

## The Lifecycle

Here's the complete timeline:

```
TIME 0:00
├─ You start Mimicus: python main.py
│
TIME 0:05
├─ You create mocks via admin API
├─ Mimicus stores them in memory
│
TIME 0:10
├─ Your frontend code runs
│
TIME 0:10:01
├─ Code requests: GET /api/users/1
│
TIME 0:10:02
├─ Mimicus receives request
├─ Searches for matching mock
├─ Finds match: "Get User"
├─ Returns response: {"id": 1, ...}
│
TIME 0:10:03
├─ Frontend code gets response
├─ Updates UI with data
│
TIME 0:10:04
└─ User sees result!
```

All of that happens in **milliseconds!**

---

## Multiple Endpoints

You can create unlimited mocks:

```
Mock 1: GET /api/users/1
Mock 2: GET /api/users/2
Mock 3: GET /api/users
Mock 4: POST /api/users
Mock 5: DELETE /api/users/1
...
```

Each request matches against all mocks, finds the best match, and responds.

Mimicus can handle:
- ✅ 10 mocks
- ✅ 100 mocks
- ✅ 1,000 mocks
- ✅ More (limited by available memory)

---

## Performance

Mimicus is **fast**:

```
Real API:
- Network latency: 50-200ms
- Database query: 10-100ms
- Processing: 10-50ms
- Total: 100-400ms

Mimicus Mock:
- Network latency: <5ms (local)
- Lookup: <1ms (in-memory)
- Response: <1ms
- Total: <5ms
```

Mocks are **80x faster** than real APIs!

---

## What Mimicus Does NOT Do

- ❌ Validate request body against schema (you can, but it's optional)
- ❌ Apply authentication/authorization (you define it)
- ❌ Persist data (unless you add state rules)
- ❌ Run business logic (unless you template it)
- ❌ Connect to databases (mocks are self-contained)

---

## The Beautiful Part

Once you set up a mock, your **code doesn't care** if it's real or fake:

```javascript
// Works the same with mocks or real API
const response = await fetch('/api/users/1');
const data = await response.json();
render(data);  // Same code for both!
```

This is why switching from mocks to real backend is **so easy**—just change one URL!

---

## Next Steps

- 💻 **[Quick Start](../getting-started/quick-start.md)** - Build your first mock
- 📊 **[Mock vs Real API](mock-vs-real-api.md)** - When to use what
- 🔧 **[Creating Mocks](../core-features/creating-mocks.md)** - Detailed guide

---

**Understanding how it works helps you use it better. You've got this!** 🚀
