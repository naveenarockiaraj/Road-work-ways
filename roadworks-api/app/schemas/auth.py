from pydantic import BaseModel, EmailStr, Field
from app.core.permissions import Role


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username or email")
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserInToken"


class UserInToken(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: Role
    is_active: bool

    model_config = {"from_attributes": True}


TokenResponse.model_rebuild()
