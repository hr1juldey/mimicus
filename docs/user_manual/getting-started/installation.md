# Installation Guide

Let's get Mimicus installed and running on your machine.

## Prerequisites

Before you start, make sure you have:

✅ **Python 3.12 or higher**
- Check: Open your terminal and run `python --version`
- If not installed: [Download Python](https://www.python.org/downloads/) and install it

✅ **Git**
- Check: Run `git --version` in terminal
- If not installed: [Download Git](https://git-scm.com/downloads)

✅ **A terminal/command line**
- Mac: Terminal app
- Windows: PowerShell or Command Prompt
- Linux: Any shell (bash, zsh, etc.)

✅ **A text editor** (optional but helpful)
- VS Code, Sublime Text, or any code editor

---

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/mimicus.git
cd mimicus
```

This downloads the Mimicus code to your computer. You're now in the `mimicus` directory.

### Step 2: Install Dependencies

Mimicus uses `uv` for dependency management. It's fast and reliable.

```bash
# Install dependencies using uv
uv sync
```

This command:
- Downloads all required libraries
- Creates a virtual environment automatically
- Prepares everything for running Mimicus

**Expected output:**
```
Resolved 42 packages in X.XXs
Prepared virtual environment in 0.XXms
```

### Step 3: Start the Server

```bash
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:18000
Press CTRL+C to quit
```

🎉 **Congratulations!** Mimicus is now running!

---

## Verify Installation

Keep the server running and open a **new terminal window**. Then run:

```bash
curl http://localhost:18000/health
```

**Expected output:**
```json
{"status": "healthy"}
```

✅ **Success!** If you see this response, Mimicus is working correctly.

---

## Access the Web UI

Open your browser and go to: **[http://localhost:18000/docs](http://localhost:18000/docs)**

You should see the Swagger UI—this is the interactive documentation for all Mimicus endpoints.

---

## Common Installation Issues

### Issue: "Python version too old"
**Solution**: Install Python 3.12+
```bash
# Check your version
python --version

# If you have multiple Python versions:
python3.12 --version  # or python3.13, etc.
```

### Issue: "uv command not found"
**Solution**: uv is installed automatically with Python. Try:
```bash
# Use Python's module runner
python -m uv sync
```

### Issue: Port 18000 already in use
**Solution**: Change the port by setting an environment variable:
```bash
# On Mac/Linux
PORT=8001 python main.py

# On Windows (PowerShell)
$env:PORT = 8001; python main.py

# On Windows (Command Prompt)
set PORT=8001 && python main.py
```

### Issue: "curl: command not found"
**Solution**: You don't need curl. Use any HTTP testing tool:
- **Browser**: Just visit `http://localhost:18000/health`
- **VS Code**: Install "REST Client" extension and create a test file
- **Postman**: [Download Postman](https://www.postman.com/downloads/) for GUI-based testing

---

## Next Steps

✅ **Server is running?** Great! Now check out:
- [Quick Start Guide](quick-start.md) - 5-minute tutorial
- [Create Your First Mock](first-mock.md) - Step-by-step walkthrough

---

## Need Help?

- 🔍 Check [Troubleshooting](troubleshooting.md)
- 📚 Read [What is Mimicus?](../concepts/what-is-mimicus.md)
- 💬 Open an issue on GitHub
