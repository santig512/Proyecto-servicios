from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatMessageCreate(BaseModel):
    chat_room_id: int
    message: Optional[str] = None
    attachment_url: Optional[str] = None

class ChatMessageRead(BaseModel):
    id: int
    chat_room_id: int
    sender_id: int
    message: Optional[str]
    attachment_url: Optional[str]
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }

class ChatRoomRead(BaseModel):
    id: int
    service_id: Optional[int]
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }
