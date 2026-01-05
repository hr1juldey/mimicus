# Create Your First Mock - Step by Step

In this guide, we'll create a complete mock for an e-commerce product endpoint. By the end, you'll understand how to build more complex mocks.

## What You'll Build

A mock API endpoint that returns product information when you request `/api/products/1`.

**Expected response:**
```json
{
  "id": 1,
  "name": "Wireless Headphones",
  "price": 79.99,
  "description": "High-quality sound with noise cancellation",
  "in_stock": true,
  "category": "Electronics"
}
```

## Prerequisites

✅ Mimicus is running
✅ You've read the [Quick Start](quick-start.md) (optional but helpful)
✅ Two terminal windows open

## Step 1: Prepare Your Mock Definition

A mock definition tells Mimicus:
- **When** to respond (what request pattern to match)
- **How** to respond (what status code and data to return)

Let's create our mock definition. Save this as `product-mock.json`:

```json
{
  "mock_name": "Get Product Details",
  "match_method": "GET",
  "match_path": "/api/products/1",
  "response_status": 200,
  "response_body": "{\"id\": 1, \"name\": \"Wireless Headphones\", \"price\": 79.99, \"description\": \"High-quality sound with noise cancellation\", \"in_stock\": true, \"category\": \"Electronics\"}"
}
```

**What each field means:**
- `mock_name` - A friendly name for this mock (use descriptive names!)
- `match_method` - HTTP method to match (GET, POST, PUT, DELETE, PATCH)
- `match_path` - The URL path to match (e.g., `/api/products/1`)
- `response_status` - HTTP status code to return (200 = success, 404 = not found, etc.)
- `response_body` - The JSON string to return (must be a string, even if it contains JSON!)

⚠️ **Important:** The `response_body` must be a JSON **string**, not a JSON object. Escape the quotes with `\"`

## Step 2: Upload the Mock to Mimicus

In your terminal (Terminal 2), run:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Get Product Details",
    "match_method": "GET",
    "match_path": "/api/products/1",
    "response_status": 200,
    "response_body": "{\"id\": 1, \"name\": \"Wireless Headphones\", \"price\": 79.99, \"description\": \"High-quality sound with noise cancellation\", \"in_stock\": true, \"category\": \"Electronics\"}"
  }'
```

**Expected response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "mock_name": "Get Product Details",
  "enabled": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

💾 **Save this ID!** You can use it to update or delete this mock later.

## Step 3: Test Your Mock

Test with curl:

```bash
curl http://localhost:18000/api/products/1
```

Or open in your browser:

```
http://localhost:18000/api/products/1
```

**Expected response:**
```json
{
  "id": 1,
  "name": "Wireless Headphones",
  "price": 79.99,
  "description": "High-quality sound with noise cancellation",
  "in_stock": true,
  "category": "Electronics"
}
```

✅ **Success!** Your first real mock is working!

---

## Step 4: Create a Variant (Optional)

Now let's add another mock for a different product. This shows how Mimicus can handle multiple mocks:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Get Product 2",
    "match_method": "GET",
    "match_path": "/api/products/2",
    "response_status": 200,
    "response_body": "{\"id\": 2, \"name\": \"Bluetooth Speaker\", \"price\": 49.99, \"description\": \"Portable speaker with 12-hour battery\", \"in_stock\": true, \"category\": \"Electronics\"}"
  }'
```

Test it:

```bash
curl http://localhost:18000/api/products/2
```

🎉 **You now have two product endpoints!**

---

## Step 5: Create a POST Mock

Let's add a mock for creating a product (POST request):

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Create Product",
    "match_method": "POST",
    "match_path": "/api/products",
    "response_status": 201,
    "response_body": "{\"id\": 3, \"name\": \"New Product\", \"price\": 0, \"in_stock\": false, \"created\": true}"
  }'
```

Test it with curl:

```bash
curl -X POST http://localhost:18000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 99.99}'
```

**Expected response:**
```json
{
  "id": 3,
  "name": "New Product",
  "price": 0,
  "in_stock": false,
  "created": true
}
```

---

## What You've Accomplished

✅ Created a complete mock API for product management
✅ Learned how to structure mock definitions
✅ Tested your mocks with curl and browser
✅ Created both GET and POST endpoints
✅ Understood how to handle different HTTP methods

---

## Key Concepts

### Mock Matching
Mimicus finds the right mock by matching:
1. **HTTP Method** (GET, POST, etc.)
2. **URL Path** (/api/products/1, etc.)

If both match, Mimicus returns that mock's response.

### Response Body
Always provide the response as a **JSON string**:
- ❌ Wrong: `{"name": "Product"}`
- ✅ Right: `"{\"name\": \"Product\"}"`

### Response Status
Common status codes:
- `200` - Success (GET, PUT, PATCH)
- `201` - Created (POST success)
- `204` - No Content
- `400` - Bad Request
- `404` - Not Found
- `500` - Server Error

---

## Next Steps

### 🔄 Make Responses More Dynamic
Your responses are currently static. Learn how to make them change:
- → [Response Templates](../core-features/response-templates.md)

### 📋 Handle More Complex Matching
Match based on headers, query params, or request body:
- → [Matching Requests](../core-features/matching-requests.md)

### 🖼️ Add Image Mocks
Need placeholder product images?
- → [Image Mocking](../image-mocking/overview.md)

### ⚛️ Use in Your Frontend
Ready to use these mocks in React or Next.js?
- → [Frontend Integration](../frontend-integration/react-setup.md)

---

## Troubleshooting

**Q: "curl: command not found"**
A: Use your browser instead, or download [Postman](https://www.postman.com/)

**Q: "Connection refused"**
A: Make sure Mimicus is running (`python main.py` in Terminal 1)

**Q: Response is different from expected**
A: Check that your `response_body` is a valid JSON **string** (with escaped quotes)

**Q: Mock created but not responding**
A: Check the URL path matches exactly (paths are case-sensitive)

More help: → [Troubleshooting Guide](troubleshooting.md)

---

**You're becoming a mock expert!** Ready to learn more advanced features? Check out [Core Features](../core-features/creating-mocks.md). 🚀
