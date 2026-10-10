from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str


class AdminDashboardResponse(BaseModel):
    message: str
    user: str