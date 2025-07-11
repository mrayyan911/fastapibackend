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