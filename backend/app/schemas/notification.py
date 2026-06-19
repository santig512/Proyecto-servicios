from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationRead(BaseModel):
    id: int
    user_id: int
    title: str
    body: Optional[str]
    type: Optional[str]
    is_read: bool
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }

class NotificationMarkRead(BaseModel):
    is_read: bool = True
