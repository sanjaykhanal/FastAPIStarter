from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import EmailStr


class LoginBase(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UpdatePassword(BaseModel):
    username: str
    old_password: str
    new_password: str
    updated_at: datetime = datetime.now()


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str


class UserBase(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    signature: Optional[str] = None
    role: Optional[str] = None


class UserCreate(LoginBase):
    username: str
    password: str
    role: Optional[str] = "admin"
    name: str
    email: EmailStr
    phone_number: str
    signature: str
    is_enabled: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class UserUpdate(UserBase):
    username: Optional[str]
    role: Optional[str]
    name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    signature: Optional[str]
    updated_at: datetime = datetime.now()


class User(BaseModel):
    id: int
    role: str
    username: str
    name: str
    email: EmailStr
    phone_number: str
    signature: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UsersListSuccessResponse(BaseModel):
    status: Optional[str] = 'success'
    data: List[User]


class UsersSuccessResponse(BaseModel):
    status: Optional[str] = "success"
    data: User


class UserDeleteSuccessResponse(BaseModel):
    status = "success"
    data: int
