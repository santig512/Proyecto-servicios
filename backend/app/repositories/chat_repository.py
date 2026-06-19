from sqlalchemy import select
from app.models.chat_room import ChatRoom
from app.models.message import Message

async def get_or_create_chat_room(db, service_id: int):
    result = await db.execute(select(ChatRoom).where(ChatRoom.service_id == service_id))
    room = result.scalars().first()
    if room:
        return room
    room = ChatRoom(service_id=service_id)
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room

async def get_messages_by_room(db, chat_room_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Message).where(Message.chat_room_id == chat_room_id).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_message(db, message_obj):
    db.add(message_obj)
    await db.commit()
    await db.refresh(message_obj)
    return message_obj
