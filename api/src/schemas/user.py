from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class UserPreferences(BaseModel):
    language: str = "en"  # en, ur
    theme: str = "light"  # light, dark, auto
    content_depth: str = "intermediate"  # beginner, intermediate, advanced
    notifications: Dict = Field(default_factory=dict)
    accessibility: Dict = Field(default_factory=dict)

class UserProfile(BaseModel):
    avatar: Optional[str] = None
    bio: Optional[str] = None
    institution: Optional[str] = None
    expertise: List[str] = Field(default_factory=list)
    learning_goals: List[str] = Field(default_factory=list)

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=255)
    role: UserRole = UserRole.STUDENT
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    profile: UserProfile = Field(default_factory=UserProfile)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    role: Optional[UserRole] = None
    preferences: Optional[UserPreferences] = None
    profile: Optional[UserProfile] = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: UserRole
    preferences: UserPreferences
    profile: UserProfile
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserAuth(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v