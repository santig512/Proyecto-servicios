from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.deps import get_current_user, get_user_from_token
from app.schemas.chat import ChatMessageCreate, ChatMessageRead, ChatRoomRead
from app.services.chat_service import ensure_chat_room, list_room_messages, send_message
from app.websocket.manager import manager

router = APIRouter()

@router.post('/rooms/{service_id}', response_model=ChatRoomRead)
async def create_room(service_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await ensure_chat_room(db, service_id)

@router.get('/rooms/{chat_room_id}/messages', response_model=list[ChatMessageRead])
async def room_messages(chat_room_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await list_room_messages(db, chat_room_id, skip, limit)

@router.post('/messages', response_model=ChatMessageRead)
async def create_message_endpoint(payload: ChatMessageCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await send_message(db, current_user.id, payload)

@router.websocket('/ws/{room_id}')
async def websocket_chat(websocket: WebSocket, room_id: str):
    token = websocket.query_params.get('token')
    db_gen = get_db()
    db = await db_gen.__anext__()
    try:
        user = await get_user_from_token(token, db) if token else None
    finally:
        await db_gen.aclose()
    if not user:
        await websocket.close(code=1008)
        return

    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room_id, f'{user.name}: {data}')
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
    except Exception:
        manager.disconnect(room_id, websocket)
