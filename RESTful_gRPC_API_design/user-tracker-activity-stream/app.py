from fastapi import FastAPI
from pydantic import BaseModel
import random
from fastapi.responses import JSONResponse

version = '/v1'

class UserCreate(BaseModel):
    name : str
    email : str
    role: str = "user"

class User(BaseModel):
    id: str
    name: str
    email: str
    role: str

class Post(BaseModel):
    id: str
    user_id: str
    title: str
    body: str    

# Memory - replace with database in production
users: dict[str, User] = {}
posts_by_user: dict[str, list[Post]] = {}

# Helpers
def generate_id(type: str) -> str:
    id = random.randint(1, 1000000)
    if type == 'user':
        id = 'u_' + str(id)
    elif type == 'post':
        id = 'p_' + str(id)
    else:
        raise ValueError(f"Invalid type: {type}")
    return id

app = FastAPI()

# Get all users
@app.get(f"{version}/users")
def get_users(limit: int = 10, offset: int = 0, role: str | None = None, sort: str | None = None, order: str | None = None):

    # Filtering
    if role:
        filtered_users = [user for user in users.values() if user.role == role]
    else:
        filtered_users = list(users.values())

    # Sorting
    if sort:

        if sort not in ["name", "email", "role"]:
            return JSONResponse(
                status_code = 400,
                content = {"error": "Sort must be 'name', 'email', or 'role'"}
            )

        if order == "asc":
            filtered_users.sort(key=lambda x: getattr(x, sort))
        elif order == "desc":
            filtered_users.sort(key=lambda x: getattr(x, sort), reverse=True)
        else:
            return JSONResponse(
                status_code = 400,
                content = {"error": "Order must be 'asc' or 'desc'"}
            )

    # Pagination
    if limit < 1 or limit > 100:
        return JSONResponse(
            status_code = 400,
            content = {"error": "Limit must be between 1 and 100"}
        )
    elif offset < 0:
        return JSONResponse(
            status_code = 400,
            content = {"error": "Offset must be >= 0"}
        )

    return JSONResponse(
        status_code = 200,
        content = [user.model_dump() for user in filtered_users][offset:offset+limit]
    )

# Create a new user
@app.post(f"{version}/users")
def add_user(user: UserCreate):

    # Validation Checks
    if user.name == "":
        return JSONResponse(
            status_code = 400,
            content = {"error": "Name is required"}
        )
    if user.email == "":
        return JSONResponse(
            status_code = 400,
            content = {"error": "Email is required"}
        )

    id = generate_id("user")
    new_user = User(id=id, **user.model_dump())
    users[id] = new_user
    posts_by_user[id] = []
    return JSONResponse(
        status_code = 201,
        content = new_user.model_dump()
    )

# Get a user by id
@app.get(f"{version}/users/{{id}}")
def get_user(id: str):
    if id not in users:
        return JSONResponse(
            status_code = 404,
            content = {"error": "User not found"}
        )
    else:
        return JSONResponse(
            status_code = 200,
            content = users[id].model_dump()
        )

# Get a user's posts
@app.get(f"{version}/users/{{id}}/posts")
def get_user_posts(id: str):
    if id not in users:
        return JSONResponse(
            status_code = 404,
            content = {"error": "User not found"}
        )
    else:
        return JSONResponse(
            status_code = 200,
            content = [post.model_dump() for post in posts_by_user[id]]
        )