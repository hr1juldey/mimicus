# Quick Start - 5 Minutes to Your First Mock

Let's build a working mock API in 5 minutes. No experience necessary!

## Prerequisites

Before starting:
- ✅ Mimicus running (follow [Installation](installation.md) if not)
- ✅ Two terminal windows open:
  - **Terminal 1**: Running `python main.py`
  - **Terminal 2**: For running commands

---

## Step 1: Create a Mock (1 minute)

In **Terminal 2**, run this command:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Get User Profile",
    "match_method": "GET",
    "match_path": "/api/users/1",
    "response_status": 200,
    "response_body": "{\"id\": 1, \"name\": \"Alice\", \"email\": \"alice@example.com\", \"role\": \"admin\"}"
  }'
```

**What this does:**
- `POST /api/admin/mocks` - Tells Mimicus to create a new mock
- `mock_name` - A friendly name for your mock
- `match_method` - This mock responds to GET requests
- `match_path` - This mock responds when path is `/api/users/1`
- `response_status` - Returns HTTP status 200 (success)
- `response_body` - The JSON data to return

**Expected response:**
```json
{
  "id": "some-uuid-here",
  "mock_name": "Get User Profile",
  "enabled": true
}
```

💡 **Tip:** Copy the response and save it somewhere—you'll need the `id` later if you want to update or delete this mock.

---

## Step 2: Test Your Mock (1 minute)

Still in **Terminal 2**, test your new mock:

```bash
curl http://localhost:18000/api/users/1
```

**Expected response:**
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "role": "admin"
}
```

✅ **Success!** Your first mock is working!

---

## Step 3: Test in Browser (1 minute)

Open your browser and visit:

```
http://localhost:18000/api/users/1
```

You should see the same JSON response.

---

## Step 4: View Your Mock in Swagger UI (1 minute)

Open your browser and visit:

```
http://localhost:18000/docs
```

You'll see the Swagger UI. Look for:
- 🔽 **GET** section
- Find `/api/users/1` endpoint
- Click "Try it out" to test it directly in the browser

---

## Step 5: Create Another Mock (1 minute)

Let's add a second mock for getting a list of users:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "List Users",
    "match_method": "GET",
    "match_path": "/api/users",
    "response_status": 200,
    "response_body": "[{\"id\": 1, \"name\": \"Alice\"}, {\"id\": 2, \"name\": \"Bob\"}]"
  }'
```

Test it:

```bash
curl http://localhost:18000/api/users
```

**Expected response:**
```json
[
  {"id": 1, "name": "Alice"},
  {"id": 2, "name": "Bob"}
]
```

---

## What You've Built

🎉 You now have a working mock API with **two endpoints**:

| Method | Path | Response |
|--------|------|----------|
| GET | `/api/users/1` | Single user (Alice) |
| GET | `/api/users` | List of users |

These mocks are now running on your local machine and responding to requests just like a real API would!

---

## Common Next Steps

### 🔄 Create a POST Mock
Need to mock creating a user? Try this:

```bash
curl -X POST http://localhost:18000/api/admin/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "mock_name": "Create User",
    "match_method": "POST",
    "match_path": "/api/users",
    "response_status": 201,
    "response_body": "{\"id\": 3, \"name\": \"Charlie\", \"created\": true}"
  }'
```

### 📝 Add Dynamic Responses
Make responses change based on input? See [Response Templates](../core-features/response-templates.md)

### 🖼️ Add Image Mocks
Need placeholder images? See [Image Mocking](../image-mocking/overview.md)

### ⚛️ Connect Your Frontend
Ready to use these mocks in React or Next.js? See [Frontend Integration](../frontend-integration/react-setup.md)

---

## Continue Learning

- 📖 [Create Your First Mock](first-mock.md) - More detailed walkthrough
- 🎯 [Core Features](../core-features/creating-mocks.md) - Learn all the capabilities
- 💬 [Concepts](../concepts/what-is-mimicus.md) - Understand how Mimicus works
- 🚨 [Troubleshooting](troubleshooting.md) - Something not working?

---

**You're doing great!** You've learned more about mocking in 5 minutes than most developers do in a day. 🚀
