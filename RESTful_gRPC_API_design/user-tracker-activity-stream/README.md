Users API (FastAPI)

Minimal REST API demonstrating versioned routes, validation, filtering, sorting, and pagination.

Run
```
uvicorn app:app --reload --port 8000
```

Endpoints
- GET /v1/users
- POST /v1/users
- GET /v1/users/{id}
- GET /v1/users/{id}/posts

Create user (JSON)
```
{
  "name": "Alice",
  "email": "alice@example.com",
  "role": "user"
}
```

Query params (GET /v1/users)
- limit: 1–100 (default 10)
- offset: >= 0 (default 0)
- role: optional filter (e.g., user, admin)
- sort: optional (name | email | role)
- order: asc | desc (used only when sort is set)

Error shape
```
{ "error": "message" }
```

Docs
- OpenAPI: http://localhost:8000/docs

