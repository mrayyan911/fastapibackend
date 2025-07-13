from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ShowUser(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    is_verified: bool

    class Config:
        from_attributes = True

from datetime import datetime

class VerificationCodeCreate(BaseModel):
    user_id: int
    code: str
    expires_at: datetime

class VerificationCode(BaseModel):
    id: int
    user_id: int
    code: str
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True
