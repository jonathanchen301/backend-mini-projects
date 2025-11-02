Users API (FastAPI)

Minimal REST API demonstrating versioned routes, validation, filtering, sorting, pagination, and JWT authentication.

Run
```
uvicorn main:app --reload --port 8000
```

Setup
- Create a `.env` file with: `SECRET_KEY=your_secret_key_here`
- Install dependencies: `pip install fastapi uvicorn pyjwt python-dotenv`

Endpoints
- POST /v1/login (public)
- GET /v1/users (public)
- POST /v1/users (public)
- GET /v1/users/{id} (public)
- GET /v1/users/{id}/posts (public)
- DELETE /v1/users/{id} (protected - Admin only)

Authentication

Login
```
POST /v1/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```

Response:
```
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

Using Tokens
Add to request headers:
```
Authorization: Bearer <your_token_here>
```

Test Credentials
- Admin: username=`admin`, password=`password` (can delete users)
- User: username=`user`, password=`password` (standard user)

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

Testing

1. Login with valid credentials
```bash
curl -X POST http://localhost:8000/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

2. Login with invalid credentials (should return 401)
```bash
curl -X POST http://localhost:8000/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrong"}'
```

3. Protected route without token (should return 401)
```bash
curl -X DELETE http://localhost:8000/v1/users/some_id
```

4. Protected route with invalid token (should return 401)
```bash
curl -X DELETE http://localhost:8000/v1/users/some_id \
  -H "Authorization: Bearer invalid_token"
```

5. Protected route with valid admin token (should succeed)
```bash
# Save token from login
TOKEN=$(curl -s -X POST http://localhost:8000/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' | jq -r '.token')

# Use token to delete
curl -X DELETE http://localhost:8000/v1/users/some_id \
  -H "Authorization: Bearer $TOKEN"
```

6. Non-admin user trying to delete (should return 403)
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"password"}' | jq -r '.token')

curl -X DELETE http://localhost:8000/v1/users/some_id \
  -H "Authorization: Bearer $TOKEN"
```

Docs
- OpenAPI/Swagger: http://localhost:8000/docs

