from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    password: str
    role: str = "customer"

class UserRead(BaseModel):
    id: int
    uuid: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    phone: Optional[str]
    role: str
    profile_image: Optional[str]
    is_active: bool
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
