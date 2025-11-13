from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    role: Role = Field(default=Role.USER)

class UserInDB(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    role: Role = Field(default=Role.USER)
    hashed_password: str = Field(...)
    disabled: bool = Field(default=False)

class UserResponse(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    role: Role = Field(default=Role.USER)
    disabled: bool = Field(default=False)

class TokenResponse(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)

class TokenData(BaseModel):
    username: Optional[str]
    role: Optional[Role]
    