# Mock vs Real API - Best Practices

Should you use mocks or a real backend? The answer: **both!** Let's figure out when to use each.

---

## Quick Decision Tree

```
Are you building frontend code?
  ├─ Yes, and backend is ready?
  │  └─ Use REAL API + optional mocks for edge cases
  ├─ Yes, but backend isn't ready?
  │  └─ Use MOCKS until backend exists
  └─ No (pure frontend work)?
     └─ Use MOCKS
```

---

## Stage-by-Stage Guide

### Stage 1: Concept & Design (No Code Yet)

**What to do:** Create mocks to validate UI/UX

```
Designer: "Here's the mockup"
Developer: "Let me create mocks that match"
Developer: "Let me build UI against mocks"
Designer: "UI looks good!" ✅
```

**Use:** 🟦 Mocks

---

### Stage 2: Active Development (Backend Not Ready)

**What to do:** Build everything with mocks

**Timeline:**
- Week 1-2: Backend team building
- Week 1-2: Frontend team building with mocks (parallel!)
- Code is independent, faster delivery

**Use:** 🟦 Mocks

---

### Stage 3: Integration Testing (Backend Ready)

**What to do:** Test with real backend

**Steps:**
1. Backend team deploys to test environment
2. Update frontend to connect to test API
3. Run full integration tests
4. Fix any mismatches

**Use:** 🟥 Real API

---

### Stage 4: QA & Edge Cases

**What to do:** Use mocks for error scenarios, real API for happy path

```javascript
// Happy path - uses real API
fetch('https://api.example.com/users');

// Error cases - use mocks locally
fetch('http://localhost:18000/users-error-500');
```

**Use:** 🟦 Mocks + 🟥 Real API

---

### Stage 5: Production

**What to do:** Real API only

**Use:** 🟥 Real API

---

## Side-by-Side Comparison

### Setup Time

| Task | Mocks | Real Backend |
|------|-------|--------------|
| Create endpoint | 30 seconds | 2-3 days |
| Add validation | 2 minutes | 1 hour |
| Add error handling | 5 minutes | 2 hours |
| Set up database | N/A | 4-6 hours |

**Mocks:** 🚀 Fast

---

### Consistency

| Scenario | Mocks | Real Backend |
|----------|-------|--------------|
| Same response every time | ✅ Yes | ❌ Varies (network, DB state) |
| Predictable timing | ✅ Yes | ❌ Varies (database load) |
| Always same format | ✅ Yes | ❌ Can change |

**Mocks:** 📊 Consistent
**Real API:** 🌍 Realistic

---

### Error Testing

| Error Case | Mocks | Real Backend |
|-----------|-------|--------------|
| API returns 500 | ✅ Easy | ❌ Hope it fails |
| Network timeout | ✅ Simulate | ❌ Hard to trigger |
| Slow response | ✅ Set delay | ❌ Rare |
| Invalid JSON | ✅ Easy | ❌ Hard to trigger |
| Missing fields | ✅ Easy | ❌ Hope it happens |

**Mocks:** 🎯 Testable
**Real API:** 🎲 Random

---

### Performance Testing

| Metric | Mocks | Real Backend |
|--------|-------|--------------|
| Response time | <5ms | 100-500ms |
| Can test UI loading state | ✅ Yes | ❌ Too fast |
| Can stress test frontend | ✅ Yes | ❌ Might DDoS backend |

**Mocks:** 💨 Fast & Safe
**Real API:** ⚠️ Slow & Risky

---

## Real-World Workflows

### Workflow 1: Parallel Development

```
Monday:
├─ Backend: Start building API
├─ Frontend: Create mocks, start building UI
│
Wednesday:
├─ Backend: API ready in staging
├─ Frontend: UI complete with mocks
│
Thursday:
├─ Frontend: Change URL to staging API
├─ Run integration tests
├─ Success! 🎉
```

**Use:** 🟦 Mocks first, then 🟥 Real API

---

### Workflow 2: Defensive Development

```
Frontend Code:
├─ Production request to real API
├─ On error, fall back to mock response
│  (shows placeholder, prevents crash)
│
User sees:
├─ Real data when API works
├─ Mock data when API fails
├─ No broken UI either way
```

```javascript
async function fetchUser() {
  try {
    const response = await fetch('https://api.example.com/user/1');
    if (!response.ok) throw new Error('Failed');
    return await response.json();
  } catch (error) {
    // Fall back to mock when real API fails
    console.warn('Using mock due to:', error);
    return { id: 1, name: 'John', email: 'john@example.com' };
  }
}
```

**Use:** 🟥 Real API with 🟦 Mock fallback

---

### Workflow 3: Feature Flags

```
Your App:
├─ New feature ready before backend
├─ Feature flag checks: is backend ready?
│  ├─ Yes: Use real API
│  └─ No: Use mocks
│
Deployment:
├─ Ship code with feature flag disabled
├─ When backend ready: enable flag
├─ No need to redeploy!
```

```javascript
const USE_REAL_API = process.env.REACT_APP_USE_REAL_API === 'true';

function fetchData() {
  const url = USE_REAL_API
    ? 'https://api.example.com/data'
    : 'http://localhost:18000/data';

  return fetch(url);
}
```

**Use:** 🟦 Mocks with feature flag, switch to 🟥 Real API

---

### Workflow 4: Comprehensive Testing

```
Test Suite:
├─ Unit tests: Use mocks (fast, isolated)
├─ Integration tests: Use real API (slower, but comprehensive)
├─ E2E tests: Use mocks (deterministic)
│
Result:
├─ Fast feedback during development
├─ Confidence before shipping
├─ No flaky tests
```

```javascript
// Unit test - use mocks
test('UserProfile displays name', async () => {
  const mockUser = { id: 1, name: 'John' };
  render(<UserProfile user={mockUser} />);
  expect(screen.getByText('John')).toBeInTheDocument();
});

// Integration test - use real API
test('UserProfile fetches and displays real data', async () => {
  render(<UserProfile userId={1} apiUrl="https://staging-api.example.com" />);
  await waitFor(() => expect(screen.getByText('John')).toBeInTheDocument());
});
```

**Use:** 🟦 Mocks for unit tests, 🟥 Real API for integration tests

---

## Migration Strategy: Mocks → Real API

### Step 1: Define Contract

```json
{
  "endpoint": "/api/users/1",
  "method": "GET",
  "expected_response": {
    "id": "number",
    "name": "string",
    "email": "string",
    "created_at": "ISO timestamp"
  }
}
```

**Who:** Frontend + Backend agree on this
**When:** Before either team codes

---

### Step 2: Build with Mocks

```bash
# Frontend team
npm run dev
# Uses http://localhost:18000/api/users/1 (mock)
```

---

### Step 3: Backend Implements

```bash
# Backend team
# Builds real API to match the contract
```

---

### Step 4: Switch URL (One Line!)

```bash
# Before
REACT_APP_API_URL=http://localhost:18000

# After
REACT_APP_API_URL=https://api.example.com

# That's it! No code changes!
```

---

### Step 5: Test Integration

```bash
# Run your existing tests
npm test

# If backend matches contract: ✅ All pass
# If backend doesn't match: ❌ Failures tell you what's wrong
```

---

## When to Keep Using Mocks

Even after real API is live:

| Scenario | Solution |
|----------|----------|
| Test error scenarios | Create error mocks locally |
| Simulate slow network | Use mock with delay |
| Feature not built yet | Mock the endpoint |
| Need to test offline | Use mocks |
| QA testing edge cases | Mock responses |
| Demo to stakeholder | Use mocks (no production data) |

---

## When to Stop Using Mocks

| Scenario | Solution |
|----------|----------|
| Code is in production | Switch to real API |
| Real users are using it | Real API required |
| Sensitive data needed | Real API only |
| Complex business logic | Real API only |

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Mocks That Don't Match Reality

```json
Mock returns:
{"id": 1, "name": "John"}

Real API returns:
{"userId": 1, "fullName": "John", "metadata": {...}}
```

**Solution:** Backend team shares API spec → Frontend creates matching mocks

### ❌ Mistake 2: Forgetting Error Cases

```javascript
// Only tested happy path with mocks
const user = await fetch('/api/user').then(r => r.json());
render(<Profile user={user.data} />);
// ^ Crashes if no data!
```

**Solution:** Create mocks that return errors, test your error handling

### ❌ Mistake 3: Different Data Types

```javascript
// Mock: returns string
response.id = "123"

// Real API: returns number
response.id = 123

// Your code expects number!
```

**Solution:** Define data types upfront in contract

### ❌ Mistake 4: Hardcoding Mocks in Code

```javascript
// ❌ Bad - mock data hidden in code
const user = { id: 1, name: 'John' };

// ✅ Good - mock from Mimicus
const response = await fetch('/api/user');
const user = await response.json();
```

**Solution:** Keep mocks in Mimicus, never hardcode data

---

## Summary Table

| Metric | Mocks | Real API |
|--------|-------|----------|
| Setup Time | ⚡ Seconds | ⏳ Days |
| Consistency | 📊 Perfect | 🌍 Realistic |
| Error Testing | ✅ Easy | ❌ Hard |
| Networking Realistic | ❌ No | ✅ Yes |
| Development Speed | 🚀 Fast | 🐢 Slow |
| Integration | ⚠️ Fragile | ✅ Solid |
| Cost | 💰 Free | 💸 Infrastructure |

---

## Best Practice: Use Both!

```
Timeline:
├─ Days 1-7: Build with 🟦 Mocks (no backend dependency)
├─ Days 5-8: Backend builds in parallel
├─ Day 8: Integrate with 🟥 Real API
├─ Day 8+: Use 🟥 Real API for production
│
Result:
├─ Frontend never blocked ✅
├─ Integration smooth ✅
├─ Code quality high ✅
└─ Time to market fast ✅
```

---

## Next Steps

- 🚀 **[Getting Started](../getting-started/quick-start.md)** - Create your first mocks
- 📝 **[Creating Mocks](../core-features/creating-mocks.md)** - Learn advanced mocking
- ⚛️ **[Frontend Integration](../frontend-integration/react-setup.md)** - Connect to your app

---

**The key insight: Mocks and real APIs aren't competing—they complement each other. Use mocks for speed during development, switch to real API for production. Best of both worlds!** 🌟
