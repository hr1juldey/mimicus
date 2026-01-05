# Response Templates - Dynamic Responses

Static responses are useful, but real APIs return different data based on requests. Let's make dynamic responses using Jinja2 templates!

---

## What are Templates?

Templates let you generate responses that **change based on the request**:

```json
Regular response:
{"id": 1, "name": "John"}  ← Always the same

Template response:
{"id": {{ request.path_params.id }}, "name": "{{ request.body.name }}"}
↑ Inserts request data here

GET /api/users/1 with body {"name": "John"} →
{"id": 1, "name": "John"}

GET /api/users/2 with body {"name": "Alice"} →
{"id": 2, "name": "Alice"}
```

---

## Simple Variable Substitution

### Using Path Parameters

```json
{
  "mock_name": "Get User by ID",
  "match_method": "GET",
  "match_path": "/api/users/{{ id }}",
  "response_body": "{\"id\": {{ request.path_params.id }}, \"name\": \"User {{ request.path_params.id }}\"}"
}
```

Request: `GET /api/users/123`
Response: `{"id": 123, "name": "User 123"}`

### Using Query Parameters

```json
{
  "mock_name": "Search Products",
  "match_method": "GET",
  "match_path": "/api/search",
  "response_body": "{\"query\": \"{{ request.query.q }}\", \"results\": []}"
}
```

Request: `GET /api/search?q=laptop`
Response: `{"query": "laptop", "results": []}`

### Using Request Body

```json
{
  "mock_name": "Create User",
  "match_method": "POST",
  "match_path": "/api/users",
  "response_body": "{\"id\": 1, \"name\": \"{{ request.body.name }}\", \"email\": \"{{ request.body.email }}\"}"
}
```

Request body: `{"name": "John", "email": "john@example.com"}`
Response: `{"id": 1, "name": "John", "email": "john@example.com"}`

---

## Conditional Logic

### if/else Statements

```json
{
  "mock_name": "Conditional Response",
  "response_body": "{% if request.query.admin == 'true' %}{\"role\": \"admin\"}{% else %}{\"role\": \"user\"}{% endif %}"
}
```

Request: `?admin=true` → `{"role": "admin"}`
Request: `?admin=false` → `{"role": "user"}`

### Checking Headers

```json
{
  "response_body": "{% if 'Authorization' in request.headers %}{\"authenticated\": true}{% else %}{\"authenticated\": false}{% endif %}"
}
```

### Multiple Conditions

```json
{
  "response_body": "{% if request.query.type == 'premium' and 'Bearer' in request.headers.get('Authorization', '') %}{\"data\": \"premium_data\"}{% else %}{\"error\": \"Unauthorized\"}{% endif %}"
}
```

---

## Loops

### Repeat Data Multiple Times

```json
{
  "response_body": "{% set count = request.query.limit | default('5') | int %}{\"items\": [{% for i in range(count) %}{\"id\": {{ i + 1 }}, \"name\": \"Item {{ i + 1 }}\"}{{ ',' if not loop.last else '' }}{% endfor %}]}"
}
```

Request: `?limit=3` →
```json
{"items": [
  {"id": 1, "name": "Item 1"},
  {"id": 2, "name": "Item 2"},
  {"id": 3, "name": "Item 3"}
]}
```

---

## Built-in Functions & Filters

### String Filters

```jinja
{{ "hello" | upper }}        → HELLO
{{ "HELLO" | lower }}        → hello
{{ "hello world" | title }}  → Hello World
{{ "hello" | length }}       → 5
{{ "hello world" | replace('world', 'mimicus') }} → hello mimicus
```

### Number Filters

```jinja
{{ 3.14159 | round(2) }}     → 3.14
{{ 9 | abs }}                → 9
{{ [1, 2, 3] | length }}     → 3
```

### Default Values

```jinja
{{ request.query.page | default('1') }}  → Uses '1' if page not provided
```

---

## Using Template Helpers

Mimicus includes helpful functions:

### Random Data

```jinja
{{ random_name() }}         → "Alice", "Bob", etc.
{{ random_email() }}        → "user@example.com"
{{ random_number(1, 100) }} → Random number 1-100
{{ random_uuid() }}         → Random UUID
```

### Date/Time

```jinja
{{ now() }}                 → Current timestamp
{{ now() | date('YYYY-MM-DD') }} → 2024-01-15
```

### List Operations

```jinja
{{ ['apple', 'banana'] | join(', ') }} → apple, banana
{{ [1, 2, 2, 3] | unique | list }} → [1, 2, 3]
```

---

## Complete Examples

### Example 1: User Profile with Conditional Role

```json
{
  "mock_name": "Get User Profile",
  "match_method": "GET",
  "match_path": "/api/users/{{ user_id }}",
  "response_body": "{\"id\": {{ request.path_params.user_id }}, \"name\": \"{{ random_name() }}\", \"email\": \"{{ random_email() }}\", \"role\": {% if request.query.admin == 'true' %}\"admin\"{% else %}\"user\"{% endif %}, \"created_at\": \"{{ now() }}\"}"
}
```

### Example 2: Paginated List

```json
{
  "mock_name": "Get Paginated Products",
  "response_body": "{\"page\": {{ request.query.page | default('1') }}, \"size\": {{ request.query.size | default('10') }}, \"total\": 100, \"items\": [{% for i in range(5) %}{\"id\": {{ i }}, \"name\": \"Product {{ i }}\"}{{ ',' if not loop.last else '' }}{% endfor %}]}"
}
```

### Example 3: Echo Request Data

```json
{
  "mock_name": "Echo Service",
  "match_method": "POST",
  "response_body": "{\"received\": {{ request.body | tojson }}, \"timestamp\": \"{{ now() }}\", \"request_id\": \"{{ random_uuid() }}\"}"
}
```

---

## Available Request Variables

```jinja
request.method          → "GET", "POST", etc.
request.path            → "/api/users/1"
request.path_params     → {"id": "1"}
request.query           → {"page": "1", "size": "10"}
request.headers         → {"Authorization": "Bearer token", ...}
request.body            → {"name": "John", ...}  (for POST/PUT)
request.remote_addr     → "192.168.1.1"
```

---

## Common Patterns

### Pattern 1: Echo Request

```json
{
  "response_body": "{\"echo\": {{ request.body | tojson }}}"
}
```

### Pattern 2: Timestamps

```json
{
  "response_body": "{\"data\": \"...\", \"created_at\": \"{{ now() | date('ISO8601') }}\", \"expires_at\": \"{{ now('days=1') | date('ISO8601') }}\"}"
}
```

### Pattern 3: Random IDs

```json
{
  "response_body": "{\"id\": \"{{ random_uuid() }}\", \"order_number\": \"ORD-{{ random_number(100000, 999999) }}\"}"
}
```

### Pattern 4: Conditional Status

```json
{
  "response_body": "{\"status\": {% if request.body.amount > 1000 %}\"pending_review\"{% else %}\"approved\"{% endif %}}"
}
```

---

## Escaping Issues

If you have literal template syntax in your response:

```jinja
Response should be: {"template": "{{ value }}"}
But gets interpreted as: value substitution

Solution: Use literal blocks
{% raw %}
{"template": "{{ value }}"}
{% endraw %}
```

---

## Debugging Templates

### Test in Swagger UI

1. Visit `http://localhost:18000/docs`
2. Create a mock with template
3. Click "Try it out"
4. See the rendered response

### Common Errors

Error: "undefined variable"
→ Check variable name spelling

Error: "Syntax error"
→ Check closing `}}`

Error: Response unchanged
→ Template not recognized (check syntax)

---

## Performance Tips

- Simple templates: Instant
- Complex loops: Use {% if limit %} for large datasets
- Avoid expensive operations in response body

---

## Next Steps

- 🌐 **[Proxy Modes](proxy-modes.md)** - Forward to real backend
- 📤 **[Bulk Import](bulk-import.md)** - Create many mocks
- 🖼️ **[Image Mocking](../image-mocking/overview.md)** - Generate images

---

**Templates unlock unlimited response variations!** 🎯
