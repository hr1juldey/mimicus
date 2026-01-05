# Bulk Import - Create Many Mocks at Once

Creating mocks one at a time is fine for a few endpoints. But what if you need to create 50 mocks? Let's bulk import from a file!

---

## Why Bulk Import?

```
Manual approach:
- Create mock 1 (1 minute)
- Create mock 2 (1 minute)
- Create mock 3 (1 minute)
... × 50
= 50 minutes ⏱️

Bulk import approach:
- Write mocks to JSON file
- Import file
= 2 minutes ⚡
```

---

## Format: JSON Array

Create a file with all your mocks:

```json
[
  {
    "mock_name": "Get User 1",
    "match_method": "GET",
    "match_path": "/api/users/1",
    "response_status": 200,
    "response_body": "{\"id\": 1, \"name\": \"Alice\"}"
  },
  {
    "mock_name": "Get User 2",
    "match_method": "GET",
    "match_path": "/api/users/2",
    "response_status": 200,
    "response_body": "{\"id\": 2, \"name\": \"Bob\"}"
  },
  {
    "mock_name": "Create User",
    "match_method": "POST",
    "match_path": "/api/users",
    "response_status": 201,
    "response_body": "{\"id\": 3, \"name\": \"Charlie\"}"
  }
]
```

---

## Import Methods

### Method 1: Using curl

```bash
curl -X POST http://localhost:18000/api/admin/mocks/import \
  -H "Content-Type: application/json" \
  -d @mocks.json
```

Or with raw JSON:

```bash
curl -X POST http://localhost:18000/api/admin/mocks/import \
  -H "Content-Type: application/json" \
  -d '[
    {"mock_name": "Get User", ...},
    {"mock_name": "Create User", ...}
  ]'
```

### Method 2: Using Swagger UI

1. Visit `http://localhost:18000/docs`
2. Find "POST /api/admin/mocks/import"
3. Click "Try it out"
4. Paste your JSON array
5. Click "Execute"

### Method 3: Using a Python Script

```python
import requests
import json

with open('mocks.json', 'r') as f:
    mocks = json.load(f)

response = requests.post(
    'http://localhost:18000/api/admin/mocks/import',
    json=mocks
)

print(response.json())
```

---

## Real-World Example

### E-Commerce Store

Create all product mocks at once:

```json
[
  {
    "mock_name": "Get Product 1",
    "match_method": "GET",
    "match_path": "/api/products/1",
    "response_body": "{\"id\": 1, \"name\": \"Laptop\", \"price\": 999.99, \"in_stock\": true}"
  },
  {
    "mock_name": "Get Product 2",
    "match_method": "GET",
    "match_path": "/api/products/2",
    "response_body": "{\"id\": 2, \"name\": \"Mouse\", \"price\": 29.99, \"in_stock\": true}"
  },
  {
    "mock_name": "Get Product 3",
    "match_method": "GET",
    "match_path": "/api/products/3",
    "response_body": "{\"id\": 3, \"name\": \"Keyboard\", \"price\": 79.99, \"in_stock\": false}"
  },
  {
    "mock_name": "Get All Products",
    "match_method": "GET",
    "match_path": "/api/products",
    "response_body": "[{\"id\": 1, \"name\": \"Laptop\", \"price\": 999.99}, {\"id\": 2, \"name\": \"Mouse\", \"price\": 29.99}, {\"id\": 3, \"name\": \"Keyboard\", \"price\": 79.99}]"
  },
  {
    "mock_name": "Create Product",
    "match_method": "POST",
    "match_path": "/api/products",
    "response_status": 201,
    "response_body": "{\"id\": 4, \"name\": \"New Product\", \"price\": 0, \"created\": true}"
  },
  {
    "mock_name": "Update Product",
    "match_method": "PUT",
    "match_path": "/api/products/1",
    "response_status": 200,
    "response_body": "{\"id\": 1, \"name\": \"Updated Laptop\", \"price\": 899.99}"
  },
  {
    "mock_name": "Delete Product",
    "match_method": "DELETE",
    "match_path": "/api/products/1",
    "response_status": 204,
    "response_body": ""
  }
]
```

Save as `products.json`, then:

```bash
curl -X POST http://localhost:18000/api/admin/mocks/import \
  -H "Content-Type: application/json" \
  -d @products.json
```

All 7 mocks created instantly! ⚡

---

## Generating Bulk Mocks Programmatically

### Python Script to Generate Mocks

```python
import json

# Generate 100 user mocks
mocks = []
for user_id in range(1, 101):
    mocks.append({
        "mock_name": f"Get User {user_id}",
        "match_method": "GET",
        "match_path": f"/api/users/{user_id}",
        "response_status": 200,
        "response_body": json.dumps({
            "id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com"
        })
    })

# Save to file
with open('bulk_users.json', 'w') as f:
    json.dump(mocks, f, indent=2)

# Or import directly
import requests
requests.post('http://localhost:18000/api/admin/mocks/import', json=mocks)
```

Result: 100 user mocks created in seconds!

---

## Import from OpenAPI Spec

If you have an OpenAPI spec, convert it to Mimicus format:

```bash
# Use a conversion tool (if available)
python convert_openapi_to_mimicus.py openapi.yaml > mocks.json

# Then import
curl -X POST http://localhost:18000/api/admin/mocks/import \
  -H "Content-Type: application/json" \
  -d @mocks.json
```

---

## Organizing Large Mock Sets

### By Feature

```
mocks/
├── users.json
├── products.json
├── orders.json
├── payments.json
└── notifications.json
```

Import each file:
```bash
curl ... -d @mocks/users.json
curl ... -d @mocks/products.json
curl ... -d @mocks/orders.json
```

### By Priority

```
mocks/
├── critical.json (priority: 100)
├── important.json (priority: 50)
└── optional.json (priority: 1)
```

### By Environment

```
mocks/
├── development/
│   └── all_mocks.json
├── staging/
│   └── realistic_mocks.json
└── testing/
    └── edge_cases.json
```

---

## Best Practices

### ✅ Do

- Use descriptive mock names
- Keep related mocks in same file
- Version control your mock definitions
- Comment your JSON file (use separate `.md` file)
- Test import before committing

### ❌ Don't

- Mix mocks with different purposes
- Leave mocks with invalid JSON
- Forget to escape quotes in response_body
- Create hundreds of mocks for same endpoint

---

## Troubleshooting

### "Import failed: Invalid JSON"

Check:
1. ✅ File is valid JSON array `[...]`
2. ✅ All strings quoted with `"`
3. ✅ All response_body values are strings (escaped JSON)
4. ✅ No trailing commas

Use online JSON validator: [jsonformatter.org](https://jsonformatter.org/)

### "Some mocks imported, some failed"

Import returns which ones failed. Fix those and re-import.

### "Duplicate mocks created"

If you import the same file twice, it creates duplicates. Either:
1. Delete existing mocks first
2. Or import with "replace" option (if available)

---

## Complete Workflow

### Step 1: Create Your Mock File

```json
[
  {
    "mock_name": "Get Users",
    "match_method": "GET",
    "match_path": "/api/users",
    "response_status": 200,
    "response_body": "[{\"id\": 1, \"name\": \"Alice\"}]"
  }
]
```

### Step 2: Validate JSON

```bash
python -m json.tool mocks.json > /dev/null && echo "Valid!"
```

### Step 3: Import

```bash
curl -X POST http://localhost:18000/api/admin/mocks/import \
  -H "Content-Type: application/json" \
  -d @mocks.json
```

### Step 4: Verify

Visit `http://localhost:18000/docs` and test your mocks.

---

## Integration with Git

Store mock definitions in version control:

```bash
git add mocks.json
git commit -m "Add 50 product mocks for e-commerce feature"
git push
```

Team members can use the same mocks:

```bash
git pull
curl ... -d @mocks.json
```

---

## Next Steps

- 🖼️ **[Image Mocking](../image-mocking/overview.md)** - Generate images
- 📚 **[API Reference](../api-reference/admin-api.md)** - Full endpoint docs
- ⚛️ **[Frontend Integration](../frontend-integration/react-setup.md)** - Use in React/Next.js

---

**Bulk import saves hours on large projects!** 🚀
