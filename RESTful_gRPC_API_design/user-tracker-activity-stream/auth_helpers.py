import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timezone, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from fastapi import HTTPException

load_dotenv()
security = HTTPBearer()

secret_key = os.getenv("SECRET_KEY")

def encode_token(payload: dict) -> str:
    payload.update({"exp": datetime.now(timezone.utc) + timedelta(days=1)})
    return jwt.encode(payload, secret_key, algorithm="HS256")

def decode_token(token: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=["HS256"])

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        return decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail = "Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code = 401, detail = "Invalid token")

def validate_admin_role(token: dict = Depends(validate_token)) -> None:
    if token["role"] != "Admin":
        raise HTTPException(status_code = 403, detail = "Admin role required")