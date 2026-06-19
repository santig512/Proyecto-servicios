from app.models.message import Message
from app.repositories.chat_repository import get_or_create_chat_room, get_messages_by_room, create_message

async def ensure_chat_room(db, service_id: int):
    return await get_or_create_chat_room(db, service_id)

async def list_room_messages(db, chat_room_id: int, skip: int = 0, limit: int = 100):
    return await get_messages_by_room(db, chat_room_id, skip, limit)

async def send_message(db, sender_id: int, message_in):
    message = Message(
        chat_room_id=message_in.chat_room_id,
        sender_id=sender_id,
        message=message_in.message,
        attachment_url=message_in.attachment_url,
    )
    return await create_message(db, message)
