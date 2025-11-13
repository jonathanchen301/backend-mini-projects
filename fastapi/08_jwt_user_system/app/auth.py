from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta, datetime, timezone
from app.models import TokenData

context = CryptContext(schemes=["bcrypt"])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return context.hash(password)

# JWT utiliies
SECRET_KEY = "VERY SECRET SECRET" # store in .env but this is a project so I leave here to show I know to do with it
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(username=payload.get("sub"), role=payload.get("role"))
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None