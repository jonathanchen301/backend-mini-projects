from app.models import UserInDB, UserCreateRequest, UserResponse
from app.auth import verify_password, get_password_hash
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models import TokenResponse
from app.auth import create_access_token
from app.dependencies import get_current_active_user, require_admin
from fastapi import Depends
from app.database import get_user, users_db

def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = get_user(username)
    if not user:
        return None
    verified = verify_password(password, user.hashed_password)
    if not verified:
        return None
    return user

app = FastAPI()

@app.post("/users", 
status_code=201,
summary="Create a new user",
description="Create a new user and store it in the database")
def create_user(user: UserCreateRequest) -> UserResponse:
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)

    user_in_db = UserInDB(
        username = user.username,
        role = user.role,
        hashed_password = hashed_password,
        disabled = False,
    )

    users_db[user.username] = user_in_db

    return UserResponse(
        username = user.username,
        role=user.role,
        disabled = False,
    )

@app.post("/auth/login", status_code=200, response_model=TokenResponse, summary="Login a user", description="Login a user and return a JWT token")
def login(request: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(
        data = {"sub": user.username, "role": user.role},
    )

    return TokenResponse(
        access_token = access_token,
        token_type = "Bearer",
    )

@app.get("/me")
def get_me(current_user = Depends(get_current_active_user)) -> UserResponse:
    return current_user

@app.get("/admin/users",
response_model=list[UserResponse],
summary="Get all users (requires admin role)",
description="Get all users from the database (requires admin role)")
def get_users(current_user = Depends(require_admin)) -> list[UserResponse]:
    return list(users_db.values())