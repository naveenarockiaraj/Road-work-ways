from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.core.permissions import Role


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8)
    role: Role = Role.SITE_ENGINEER


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: Role
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
