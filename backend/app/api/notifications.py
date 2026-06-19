from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.deps import get_current_user
from app.schemas.notification import NotificationMarkRead, NotificationRead
from app.services.notification_service import list_user_notifications, mark_notification
from app.repositories.notification_repository import get_notification_by_id

router = APIRouter()

@router.get('/', response_model=list[NotificationRead])
async def my_notifications(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await list_user_notifications(db, current_user.id)

@router.patch('/{notification_id}', response_model=NotificationRead)
async def mark_read(notification_id: int, payload: NotificationMarkRead, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    notification = await get_notification_by_id(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail='Notification not found')
    if notification.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Forbidden')
    return await mark_notification(db, notification, payload)
