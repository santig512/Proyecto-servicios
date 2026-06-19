from app.repositories.notification_repository import (
    get_notifications_by_user,
    get_notification_by_id,
    update_notification,
    get_non_admin_users,
    create_notifications,
)
from app.models.notification import Notification

async def list_user_notifications(db, user_id: int, skip: int = 0, limit: int = 100):
    return await get_notifications_by_user(db, user_id, skip, limit)

async def mark_notification(db, notification, payload):
    data = payload.model_dump(exclude_unset=True)
    return await update_notification(db, notification, data)


async def notify_non_admin_users(db, title: str, body: str, notification_type: str = 'service'):
    users = await get_non_admin_users(db)
    notifications = [
        Notification(user_id=user.id, title=title, body=body, type=notification_type)
        for user in users
    ]
    return await create_notifications(db, notifications)
