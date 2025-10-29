from fastapi import FastAPI
from pydantic import BaseModel
import random
from fastapi.responses import JSONResponse

version = '/v1'

class UserCreate(BaseModel):
    name : str
    email : str

class User(BaseModel):
    id: str
    name: str
    email: str

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
def get_users():
    return JSONResponse(
        status_code = 200,
        content = [user.model_dump() for user in users.values()]
    )

# Create a new user
@app.post(f"{version}/users")
def add_user(user: UserCreate):
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