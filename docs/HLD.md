# High-Level Design: FastAPI Universal Mock & Mimic

## 1. Executive summary / Purpose

A configurable FastAPI service that can **mock and mimic any HTTP API in the world** for frontend engineers and integration teams while the real backend is unavailable. It should be easy to configure, switch between mock/proxy/real modes, support stateful flows, replay/record traffic, import OpenAPI/Swagger definitions, provide a friendly admin UI and API for managing mocks, and be production-grade enough for CI tests and staging.

This document covers feasibility, architecture, components, data models, configuration formats, runtime behaviours, security, deployments, operations and trade-offs.

---

## 2. Feasibility

**Short answer:** Highly feasible.

**Why feasible:**

* FastAPI is asynchronous, lightweight, and fast — excellent for HTTP mocking, proxying, and hosting admin APIs.
* The problem is mostly engineering: design a rich configuration schema + a flexible runtime engine that matches incoming requests to configured mock rules and generates responses (static or dynamic). Libraries exist for templating (Jinja2), request/response manipulation, and OpenAPI parsing.
* Core challenges are not technical show-stoppers: handling *very* complex backend logic, stateful domain behavior, data consistency, security isolates, and scale under heavy synthetic load.

**Constraints & trade-offs:**

* Simple stateless mocks (status codes, bodies, delays) are trivial. Full fidelity (business rules, database transactions, complex authentication flows) becomes progressively more expensive and may require embedding small scripts, a sandboxed runtime, or attaching to a test database.
* Security: exposing sensitive behaviour or proxying production can leak data if not carefully isolated.
* Performance: for heavy load, must scale horizontally and use robust match/index strategies (Radix trees, hashing) and caching.

**Recommended minimal viable scope (MVP):**

* Route matching by path/method + OpenAPI import.
* Static responses + templated dynamic responses (Jinja2) with variable substitution from request.
* Toggle per-route between `mock`, `proxy`, and `passthrough` modes.
* Simple state store (Redis or SQLite) for sessions and sequence flows.
* Admin REST API + small React admin UI to add/modify mocks and import OpenAPI.

---

## 3. Goals and non-goals

**Goals (must-have):**

* Easy creation and management of mocks via REST API and Admin UI.
* Import OpenAPI/Swagger to scaffold mocks automatically.
* Dynamic templating of responses including data from request, sequence counters, and persisted state.
* Toggleable runtime modes: `mock only`, `proxy-with-fallback`, `record` (record responses), `replay`.
* Support for delays, errors, throttling and rate-limiting simulations.
* Versioning & environment overrides (dev/staging/ci).
* Observability: logging, request inspector, metrics.

**Non-goals (out-of-scope for MVP):**

* Full replacement of complex backend logic (e.g. long-running batch jobs, event-sourced workflows) — these should be approximated or delegated to small helper microservices.
* Running untrusted arbitrary code in production without sandboxing.

---

## 4. High-level architecture

Components:

1. **FastAPI Mock Engine (Core)** — main HTTP entrypoint handling incoming requests and returning mock/proxied responses.
2. **Admin API** — a set of REST endpoints for CRUD on mock definitions, imports, toggles, and management.
3. **Admin UI** — React-based UI for human-friendly creation and testing of mocks.
4. **Config Store** — persisted store for mock definitions and scenario state. (Postgres or SQLite for metadata; Redis for ephemeral session/state.)
5. **Template Engine** — Jinja2 for response templating + helpers for common functions (random, faker, timestamp).
6. **Matcher/Router** — efficient runtime matcher to find the right mock rule for an incoming request.
7. **Proxy / Recorder** — optional module to forward unmatched requests to a real backend and optionally record responses.
8. **Scripting / Plugins (optional)** — sandboxed Python or JS scripts for advanced logic.
9. **Observability** — structured logs, Prometheus metrics, and request traces.
10. **CI/CD / CLI** — tools to import/export sets of mocks; run locally with a single command.

Flow:

* Incoming request -> Matcher finds best mock rule -> Rule defines: static/template response OR proxy-to-backend OR call script -> apply response modifiers (delay, headers, status) -> persist state if configured -> return response.

---

## 5. Data model and configuration

Represent mocks as typed JSON/YAML (easier to edit and import/export). Example top-level objects:

**MockDefinition (schema):**

* `id`: uuid
* `name`: string
* `priority`: integer (higher = earlier)
* `enabled`: bool
* `match`: { `method`, `path` (template/regex), `headers`, `query`, `body` (jsonpath/regex), `content_type` }
* `mode`: enum(`mock`, `proxy`, `record`, `passthrough`) // per-route
* `response`: {

  * `status`: int
  * `headers`: map
  * `body`: string | object (can be Jinja template)
  * `delay_ms`: int
  * `repeat_policy`: { `sequence`: true/false, `loop`: boolean }
  * `variants`: [ { `weight` , response } ]
    }
* `state`: { `persist_to`: `redis` | `db`, `keys`: [..] }
* `hooks`: { `before`: script-id, `after`: script-id }
* `created_by`, `tags`, `version`

**Example YAML:**

```yaml
- id: auth-login-success
  name: "Login success"
  priority: 100
  enabled: true
  match:
    method: POST
    path: /api/v1/auth/login
    body:
      jsonpath: $.username
      equals: "test@example.com"
  mode: mock
  response:
    status: 200
    headers:
      Content-Type: application/json
    body: |
      {
        "token": "{{ random_token() }}",
        "user": {"id": "u-123","email": "{{ request.json.username }}"}
      }
    delay_ms: 120
```

**OpenAPI import:** Convert each operation -> a MockDefinition skeleton with example responses.

---

## 6. Matching & routing rules

* Support path templates (`/users/{id}`) and regexes.
* Support content-based matching: query, headers, JSONPath on body, or full body regex.
* Matching priority: exact matches > path templates > regex. Use `priority` override for tie-breaking.
* Provide `matchScore` debugging in logs so devs can see why a route matched.

**Optimization:** Build separate indexes: method->path trie -> candidate rules. For body-based matching, only evaluate after path/method match.

---

## 7. Response generation

**Types:** static, templated, variant-weighted, scripted

**Templating:** Use Jinja2 with a controlled context exposing:

* `request`: headers, query, path_params, json, raw_body
* helpers: `random_token()`, `faker()`, `now()`, `inc(key)`, `state.get(key)`, `state.set(key, value)`

**Variants:** support multiple variants with weights for A/B test or chaos simulation.

**Delays & errors:** built-in fields to inject delays, throttling, intermittent 5xx/4xx to test error handling.

---

## 8. State & sequences

For flows that must be stateful (e.g., OTP flows, multi-step forms):

* Provide a state store using Redis (recommended) or SQLite for local runs.
* Key patterns: `session:{session_id}:...` or `mock:{mock_id}:counter`.
* Provide built-in atomic ops (incr, compare-and-set) for sequencing.
* Allow scoping of state by `session`, `client-ip`, or explicit header.

---

## 9. Proxying & recording (swap to real)

**Modes:**

* `mock` — always return configured response.
* `proxy` — forward request to `upstream_url` and return response. Optionally record into a mock object.
* `proxy-with-fallback` — attempt real upstream; if it fails or times out, return configured fallback mock.
* `record` — forward and save recorded response to create skeleton mocks (useful in initial setup).

**Swap strategy for frontend:**

* Frontend points to the Mock Service URL. To move to real backend, either:

  * Update environment variable to point to real backend URL and switch the mock instance to `proxy`/`passthrough`. OR
  * Disable mock routes and point frontend to real service directly.

Prefer toggling route `mode` for incremental migration.

---

## 10. Admin API & UX

**Admin REST endpoints (examples):**

* `GET /api/admin/mocks` — list
* `POST /api/admin/mocks` — create
* `GET /api/admin/mocks/{id}` — view
* `PUT /api/admin/mocks/{id}` — update
* `DELETE /api/admin/mocks/{id}` — delete
* `POST /api/admin/import/openapi` — import
* `POST /api/admin/record/start` — start recording
* `POST /api/admin/record/stop` — stop recording
* `POST /api/admin/activate/{id}` — toggle
* `POST /api/admin/activate/bulk` — environment promotion
* `GET /api/admin/inspector?trace_id=...` — view recorded request/response

**Admin UI features:**

* Route list with quick-enable/disable and toggle mock/proxy
* Route editor with a playground (send test requests, see response, view logs)
* Import OpenAPI button that scaffolds mocks
* Versioning & environment promotion (promote dev mocks -> staging)
* Traffic inspector and recorded traces

---

## 11. Security

* Admin API protected by API key or OAuth; integrate with SSO (OIDC) for enterprise.
* Support role-based access: read-only vs editor vs admin.
* Protect proxying to upstreams: whitelist allowed upstream domains, do not proxy to private networks by default.
* Sandbox any scripting capabilities. If allowing Python/JS hooks, run in a restricted environment (e.g., WASM, or limited subprocess with strict resource limits) or only enable in trusted environments.
* Input validation on all admin inputs; rate-limit public endpoints to mitigate abuse.

---

## 12. Observability & debugging

* Structured logs (JSON) with correlation IDs.
* Prometheus metrics: requests, latencies, match counts, error rates, number of mocks.
* Request Inspector UI: shows request, matched mock, generated response, evaluation traces (which match conditions triggered), and template context.
* Export traces: link tracing to Jaeger/OpenTelemetry.
* Audit logs for admin actions.

---

## 13. Testing & QA

* Unit tests for matcher, template rendering, and proxying.
* Contract tests: use imported OpenAPI to validate mock responses conform to schema (jsonschema).
* End-to-end tests: spin up a local instance via Docker Compose and run frontend tests against it.
* Fuzz tests: randomize variant weights, inject delays to test front-end resilience.

---

## 14. Deployment & scaling

**Local developer:** Docker Compose using SQLite (or local Postgres) + Redis.

**Staging/Production:**

* Deploy on Kubernetes with Horizontal Pod Autoscaler for CPU and request concurrency.
* Use an ingress (Traefik / Nginx) and TLS.
* Use Redis for state, Postgres for metadata, object storage for recorded responses.
* Use sidecar/ingress to expose admin UI only to internal networks.

**Performance considerations:**

* Keep template rendering fast; cache compiled templates.
* For high throughput, avoid heavy per-request Python logic; use worker pools for expensive tasks (recording, script execution).
* Use uvicorn/gunicorn (uvicorn workers) and async endpoints.

---

## 15. Extensibility & integrations

* Import/Export YAML/JSON for mocks.
* CLI: `mockctl` to list/create/delete mocks.
* Integrations: Git-backed mock repository (gitops) for declarative mocks and environment promotion.
* Webhooks: send events on record/create/mock-change.
* VS Code extension (future) to browse and edit mocks from editor.

---

## 16. Example mock definitions (more advanced)

**Sequence / OTP flow:**

```yaml
- id: otp-send
  name: "OTP Send"
  match:
    method: POST
    path: /api/v1/otp
    body:
      jsonpath: $.phone
  response:
    status: 200
    body: "{ \"status\": \"sent\" }"
  state:
    persist_to: redis
    keys:
      - session: "otp:{{ request.json.phone }}"
  hooks:
    after: generate-and-store-otp # script uses state.set

- id: otp-verify
  name: "OTP Verify"
  match:
    method: POST
    path: /api/v1/otp/verify
    body:
      jsonpath: $.code
  response:
    status: 200
    body: |
      {
        "ok": {{ state.get("otp:{{ request.json.phone }}") == request.json.code }}
      }
```

**Proxy-with-fallback:**

```yaml
- id: products-list
  match:
    method: GET
    path: /api/v1/products
  mode: proxy-with-fallback
  upstream: https://real-api.example.com
  response:
    fallback:
      status: 200
      body: "[]"
```

---

## 17. Admin UX: How frontend engineers will use it

1. Import the project's OpenAPI file -> scaffold mocks.
2. Use Admin UI to tweak responses or set templated dynamic fields.
3. Point local frontend to Mock Service URL (or set environment variable `API_BASE_URL=http://localhost:8000`).
4. Toggle a route from `mock` to `proxy` for partial integration with real backend; use proxy-with-fallback while backend is flaky.
5. Use request inspector to debug mismatches.

---

## 18. Risks & mitigations

* **Risk:** Sensitive data leak when recording real upstream responses. *Mitigation*: Sanitize/obfuscate recorded payloads; store recordings in private buckets; only enable recording in non-prod.
* **Risk:** Arbitrary script execution can escalate. *Mitigation*: Sandbox scripts; prefer declarative templating + helper functions.
* **Risk:** Complex business logic impossible to mock perfectly. *Mitigation*: Use small test doubles (mini-services) for complex workflows, or maintain a shared test DB.

---

## 19. Roadmap (phased)

**Phase 0 (2–3 weeks):** MVP CLI + FastAPI core

* Basic matcher, static/templated responses, YAML/JSON definitions, simple Redis state, admin REST API.

**Phase 1 (3–4 weeks):** Admin UI + OpenAPI import

* React UI, import OpenAPI, playground, versioning and environment promotion.

**Phase 2 (3–4 weeks):** Proxy/Record, sequence flows

* Proxy-with-fallback, recording pipeline, stateful flows.

**Phase 3 (ongoing):** Sandboxed scripting, GitOps, K8s helm chart, enterprise features (SSO, RBAC).

---

## 20. Implementation tech stack (suggested)

* Python + FastAPI, Uvicorn
* Pydantic for config schemas
* Jinja2 for template rendering
* Redis for state, Postgres for metadata, S3-compatible storage for recordings
* React + Vite for Admin UI (or shadcn/ui if you want a polished design)
* Docker Compose for local dev, Kubernetes / Helm for production
* OpenTelemetry + Prometheus + Grafana for observability

---

## 21. Appendices

### A. Minimal example of runtime toggle (pseudo-code)

```back
# env: MOCK_MODE=enabled
route = find_route(req)
if route.mode == 'mock':
    return render(route.response)
elif route.mode == 'proxy':
    return proxy_to_upstream(req, route.upstream)
elif route.mode == 'proxy-with-fallback':
    try:
        return proxy_to_upstream(req)
    except TimeoutError:
        return render(route.response.fallback)
```

### B. Recommended small dev commands

* `docker-compose up` — start local mock service
* `mockctl import openapi ./openapi.yaml` — import
* `mockctl export ./mocks.yaml` — export current mocks

---

## Conclusions

Building a universal mock & mimic service with FastAPI is practical and will deliver large productivity gains for frontend and integration teams. The engineering complexity rises with fidelity — for many teams, a feature-complete MVP (templated responses, OpenAPI import, proxying, and stateful flows via Redis) will be sufficient.
