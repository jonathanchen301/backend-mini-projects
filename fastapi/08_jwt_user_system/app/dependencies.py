from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.models import UserResponse, Role
from app.auth import decode_access_token
from fastapi import HTTPException
from app.database import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    data = decode_access_token(token)
    if not data:  
        raise HTTPException(status_code=401, detail="Invalid token")
    if not data.username:
        raise HTTPException(status_code=401, detail="Invalid username")
    user = get_user(data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    return UserResponse(
        username=user.username,
        role=user.role,
        disabled=user.disabled
    )

def get_current_active_user(current_user = Depends(get_current_user)) -> UserResponse:
    if current_user.disabled:
        raise HTTPException(status_code=401, detail="User is disabled")
    return current_user

def require_admin(current_user = Depends(get_current_active_user)) -> UserResponse:
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin role required")
    return current_user