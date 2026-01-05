# Troubleshooting Guide

Something not working? Let's fix it!

---

## Server Won't Start

### Error: "Address already in use"

**Problem:** Port 18000 is already being used by another application.

**Solution 1: Change the Port**

```bash
# Linux/Mac
PORT=8001 python main.py

# Windows (PowerShell)
$env:PORT = 8001; python main.py

# Windows (Command Prompt)
set PORT=8001 && python main.py
```

Then access Mimicus at `http://localhost:8001`

**Solution 2: Find and Stop the Application Using Port 18000**

```bash
# Mac/Linux - find what's using port 18000
lsof -i :18000

# Windows - find what's using port 18000
netstat -ano | findstr :18000

# Then stop the application or kill the process
kill <process-id>  # On Mac/Linux
taskkill /PID <process-id> /F  # On Windows
```

---

## Connection Problems

### Error: "Connection refused" or "Can't reach server"

**Problem:** Mimicus isn't running or you're using the wrong URL.

**Solution:**

1. ✅ Make sure Terminal 1 shows `Uvicorn running on http://0.0.0.0:18000`
2. ✅ Wait 5 seconds after starting (server needs startup time)
3. ✅ Try in a new terminal: `curl http://localhost:18000/health`
4. ✅ Check the URL has no typos (case-sensitive!)

**Expected response:**
```json
{"status": "healthy"}
```

---

### Error: "Connection timed out"

**Problem:** Firewall or network issue.

**Solution:**

1. Check if firewall is blocking port 18000
2. On Mac: System Preferences → Security & Privacy → Firewall
3. On Windows: Windows Defender Firewall → Allow an app through firewall
4. Try `http://127.0.0.1:18000` instead of `http://localhost:18000`

---

## Mock Creation Issues

### Mock Created but Not Responding

**Problem:** You created a mock, but requests aren't matching.

**Solution:**

1. **Verify the exact path** (paths are case-sensitive!)
   ```bash
   # Created with: /api/users/1
   # Test with: GET /api/users/1
   # Wrong: /api/Users/1 or /api/users/1/ (with trailing slash)
   ```

2. **Check the HTTP method**
   ```bash
   # If you created a GET mock, don't test with POST
   curl -X GET http://localhost:18000/api/users/1
   ```

3. **List all mocks to see what's created**
   ```bash
   curl http://localhost:18000/api/admin/mocks
   ```

4. **Check if mock is enabled**
   - Look at the response from step 3
   - Make sure `"enabled": true`

---

### Error: "Invalid JSON in response_body"

**Problem:** Your response_body isn't properly formatted as a JSON string.

**Solution:**

The `response_body` must be a **JSON string**:

```bash
# ❌ Wrong - this is a JSON object, not a string
"response_body": {"id": 1, "name": "John"}

# ✅ Right - this is a JSON string
"response_body": "{\"id\": 1, \"name\": \"John\"}"
```

**Quick fix:** Use an online [JSON escape tool](https://jsonformatter.org/json-escape) to convert your JSON to a properly escaped string.

---

## curl Problems

### Error: "curl: command not found"

**Problem:** curl isn't installed on your computer.

**Solution 1: Install curl**

```bash
# Mac (with Homebrew)
brew install curl

# Windows - use PowerShell's Invoke-WebRequest instead
Invoke-WebRequest -Uri http://localhost:18000/health

# Linux (Debian/Ubuntu)
sudo apt-get install curl
```

**Solution 2: Use Your Browser Instead**

Just visit the URL in your web browser:
```
http://localhost:18000/api/users/1
```

**Solution 3: Use Postman**

Download [Postman](https://www.postman.com/downloads/) for a GUI tool instead of curl.

---

## Response Issues

### Response Shows as Plain Text, Not JSON

**Problem:** Browser is displaying JSON as plain text instead of pretty-printed.

**Solution:**

1. Install "JSON Formatter" browser extension
2. Or access the Swagger UI instead: `http://localhost:18000/docs`

---

### Mock Returns Wrong Data

**Problem:** Created mock returns unexpected response.

**Solution:**

1. **Double-check the response_body**
   ```bash
   # View all mocks
   curl http://localhost:18000/api/admin/mocks

   # Find your mock and verify the response_body matches expectations
   ```

2. **Update the mock if needed**
   ```bash
   curl -X PUT http://localhost:18000/api/admin/mocks/<mock-id> \
     -H "Content-Type: application/json" \
     -d '{
       "mock_name": "Updated Name",
       "match_method": "GET",
       "match_path": "/api/users/1",
       "response_status": 200,
       "response_body": "{\"id\": 1, \"name\": \"John Doe\"}"
     }'
   ```

---

## Python/Installation Issues

### Error: "Python version too old"

**Problem:** You have Python 3.11 or older, but Mimicus needs 3.12+.

**Solution:**

1. Install Python 3.12 or higher from [python.org](https://www.python.org/downloads/)
2. After installation, verify:
   ```bash
   python3.12 --version
   ```
3. If you have multiple Python versions, use the full version:
   ```bash
   python3.12 main.py
   ```

---

### Error: "uv sync failed"

**Problem:** Dependency installation failed.

**Solution:**

1. Update Python:
   ```bash
   python --version  # Should be 3.12+
   ```

2. Try manual installation:
   ```bash
   pip install -r requirements.txt
   ```

3. If that fails, try:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

---

## Docker Issues (If Running in Docker)

### Container Won't Start

```bash
# View container logs
docker logs mimicus

# Check if port is in use
docker ps -a

# Remove old container and try again
docker-compose down
docker-compose up -d
```

---

## Still Need Help?

- 📖 Read the [Concepts](../concepts/what-is-mimicus.md) section
- 🔍 Check the [API Reference](../api-reference/admin-api.md)
- 💬 Open an issue on [GitHub](https://github.com/your-org/mimicus/issues)
- 📧 Contact the team

---

## Report a Bug

If you found an actual bug:

1. Go to [GitHub Issues](https://github.com/your-org/mimicus/issues)
2. Click "New Issue"
3. Describe:
   - What you were trying to do
   - What error you got
   - Your Python version (`python --version`)
   - Your operating system (Mac/Windows/Linux)

This helps us fix problems faster!

---

**Still stuck?** Don't give up! Reach out to the community or open an issue. We're here to help! 🚀
