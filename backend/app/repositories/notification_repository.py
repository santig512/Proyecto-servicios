from sqlalchemy import select
from app.models.user import User
from app.models.notification import Notification

async def get_notifications_by_user(db, user_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_notification_by_id(db, notification_id: int):
    result = await db.execute(select(Notification).where(Notification.id == notification_id))
    return result.scalars().first()

async def update_notification(db, notification_obj: Notification, updates: dict):
    for field, value in updates.items():
        setattr(notification_obj, field, value)
    await db.commit()
    await db.refresh(notification_obj)
    return notification_obj


async def get_non_admin_users(db):
    result = await db.execute(select(User).where(User.role != 'admin'))
    return result.scalars().all()


async def create_notifications(db, notifications: list[Notification]):
    if not notifications:
        return []
    db.add_all(notifications)
    await db.commit()
    for notification in notifications:
        await db.refresh(notification)
    return notifications
