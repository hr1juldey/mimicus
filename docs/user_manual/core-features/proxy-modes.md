# Proxy Modes - Bridge to Real APIs

What if you can't mock everything? Proxy mode lets Mimicus forward unmatched requests to a real backend!

---

## The Problem

You've mocked 80% of your API endpoints, but the remaining 20% are complex. You have two choices:

```
Option 1: Mock everything (weeks of work)
Option 2: Mock what you can, forward the rest to real API
```

Proxy mode = **Option 2**

---

## How Proxy Mode Works

```
Your Code
  ↓
Request to Mimicus
  ↓
Does Mimicus have a mock?
  ├─ YES → Return mocked response
  └─ NO  → Forward to real backend → Return real response
```

Your code sees the same responses whether they're mocked or proxied!

---

## Basic Setup

### Step 1: Configure Upstream URL

Set the upstream (real backend) URL:

```json
{
  "config_upstream_url": "https://api.example.com"
}
```

This can be set via:
- Environment variable: `CONFIG_UPSTREAM_URL`
- Config file
- Runtime settings

### Step 2: Create Mocks for What You Need

```json
{
  "mock_name": "Get User (Mocked)",
  "match_method": "GET",
  "match_path": "/api/users/1",
  "response_status": 200,
  "response_body": "{\"id\": 1, \"name\": \"John\"}"
}
```

### Step 3: Everything Else Proxies

```
GET /api/users/1
→ Matches mock → Returns mock ✅

GET /api/users/2
→ No mock → Forwards to https://api.example.com/api/users/2 → Returns real data ✅

GET /api/products/advanced/search
→ No mock → Forwards to real backend ✅
```

---

## Example: Partial Mocking

Your team is ready to build, but backend only has user endpoints ready.

**Setup:**

```json
{
  "config_upstream_url": "https://staging-api.example.com"
}
```

**Mocks you create:**

```json
[
  {
    "mock_name": "Get User Profile",
    "match_path": "/api/users/1",
    "response_body": "{\"id\": 1, \"name\": \"John\"}"
  },
  {
    "mock_name": "Create Order",
    "match_path": "/api/orders",
    "match_method": "POST",
    "response_body": "{\"id\": 123, \"status\": \"created\"}"
  }
]
```

**What happens:**

```
GET /api/users/1
→ Mocked ✅

GET /api/products (not mocked)
→ Proxied to https://staging-api.example.com/api/products ✅

POST /api/orders
→ Mocked ✅

PUT /api/products/1 (not mocked)
→ Proxied to https://staging-api.example.com/api/products/1 ✅
```

---

## Per-Mock Proxy Configuration

You can also proxy individual requests:

```json
{
  "mock_name": "Proxy Search Endpoint",
  "match_method": "POST",
  "match_path": "/api/search",
  "proxy_to_upstream": "https://api.example.com",
  "pass_through_request": true,
  "pass_through_headers": true
}
```

**Options:**

```json
{
  "proxy_to_upstream": "https://real-api.example.com",
  "pass_through_request": true,    // Forward request body as-is
  "pass_through_headers": true,    // Forward request headers
  "modify_upstream_url": "/v2/api" // Change path to /v2/api
}
```

---

## Fallback Strategy

```
Client Request
  ↓
Try Mock Match
  ├─ Found → Return mock ✅
  └─ Not found → Try Upstream
      ├─ Upstream responds → Return response ✅
      └─ Upstream fails → Return error
```

---

## Use Cases

### Use Case 1: Gradual Migration

Your frontend is currently using a mock API. Real backend is being built.

```
Day 1-5: Everything is mocked
Day 5+: Real backend gradually goes live
  ├─ Mock high-priority endpoints
  └─ Proxy everything else to staging

Week 2: Real backend is stable
  └─ Switch to 100% real API
```

### Use Case 2: Multiple Backends

Your app calls different services:

```
Mimicus configuration:
{
  "upstreams": {
    "default": "https://api.example.com",
    "payments": "https://payments.example.com"
  }
}

Mock easy endpoints locally
Proxy complex payment logic to payment service
Proxy notifications to notification service
```

### Use Case 3: Legacy System Integration

You're building new frontend for legacy backend.

```
Real backend: Slow, complex, hard to test
Solution:
  ├─ Mock new endpoints you're building
  └─ Proxy existing endpoints to legacy system
```

---

## Headers and Request Forwarding

### Preserve Request Headers

```json
{
  "mock_name": "Proxy with Auth",
  "match_path": "/api/protected",
  "pass_through_headers": true,  // Forward Authorization header, etc.
  "proxy_to_upstream": "https://api.example.com"
}
```

Your request headers get forwarded to backend.

### Modify Headers Before Proxying

```json
{
  "mock_name": "Add API Key",
  "match_path": "/api/data",
  "proxy_to_upstream": "https://api.example.com",
  "proxy_headers": {
    "X-API-Key": "secret123"
  }
}
```

Adds `X-API-Key` header before forwarding.

---

## Response Modification

### Intercept and Modify

```json
{
  "mock_name": "Proxy with Transform",
  "match_path": "/api/users",
  "proxy_to_upstream": "https://api.example.com",
  "transform_response": true,
  "response_body": "{% set upstream = upstream_response %}{\"data\": {{ upstream | tojson }}, \"transformed\": true}"
}
```

---

## Timeout Handling

```json
{
  "proxy_to_upstream": "https://api.example.com",
  "upstream_timeout_ms": 5000,  // Wait max 5 seconds
  "upstream_timeout_response": "{\"error\": \"Upstream timeout\"}"
}
```

If backend takes >5 seconds, return timeout response.

---

## Performance Considerations

**Mock vs Proxy response times:**

```
Mock:        <5ms   (instant)
Proxy:     100-500ms (network latency + processing)
```

For maximum speed:
- Mock frequently-used endpoints
- Proxy less-critical ones

---

## Troubleshooting

### "Proxying not working"

Check:
1. ✅ `config_upstream_url` is set
2. ✅ URL is correct and reachable
3. ✅ No firewall blocking
4. ✅ Backend is running

### "Mock is matching instead of proxying"

This is correct! Mocks have priority. Remove/disable the mock to proxy.

### "Headers not being forwarded"

```json
{
  "pass_through_headers": true,  // Add this
  "proxy_to_upstream": "https://api.example.com"
}
```

### "Upstream returns 403"

Backend is rejecting the request. Check:
- Authentication headers
- API keys
- Authorization rules

---

## Best Practices

### ✅ Do

- Mock high-value endpoints (used frequently)
- Proxy complex endpoints (less frequent)
- Test both mocked and proxied paths
- Monitor upstream failures

### ❌ Don't

- Proxy everything (defeats purpose)
- Forget to add authentication headers
- Proxy without timeout (can hang indefinitely)
- Use proxy as substitute for error handling

---

## Migration Path: Mock → Proxy → Real

```
Phase 1: Everything Mocked
  ├─ Zero backend dependency
  └─ Fast development

Phase 2: Partial Mocking + Proxy
  ├─ Mock what you need
  ├─ Proxy to staging backend
  └─ Still independent

Phase 3: 100% Real API
  ├─ Disable Mimicus
  └─ Or keep it for local testing
```

---

## Next Steps

- 📤 **[Bulk Import](bulk-import.md)** - Create many mocks at once
- 🖼️ **[Image Mocking](../image-mocking/overview.md)** - Generate images
- 📚 **[API Reference](../api-reference/admin-api.md)** - Full endpoint docs

---

**Proxy mode gives you the best of both worlds: speed of mocks + flexibility of real backends!** 🚀
