from sqlalchemy import select, delete, update
from app.models.user import User
from app.database.session import AsyncSessionLocal
from app.models.address import Address
from app.models.audit_log import AuditLog
from app.models.message import Message
from app.models.notification import Notification
from app.models.review import Review
from app.models.service import Service
from app.models.technician_availability import TechnicianAvailability

async def get_user_by_email(db, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db, user_obj):
    db.add(user_obj)
    await db.commit()
    await db.refresh(user_obj)
    return user_obj

async def get_user(db, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_users(db, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db, user_obj: User, updates: dict):
    for field, value in updates.items():
        setattr(user_obj, field, value)
    await db.commit()
    await db.refresh(user_obj)
    return user_obj


async def delete_user(db, user_obj: User):
    await db.execute(delete(Address).where(Address.user_id == user_obj.id))
    await db.execute(delete(Notification).where(Notification.user_id == user_obj.id))
    await db.execute(delete(Message).where(Message.sender_id == user_obj.id))
    await db.execute(delete(Review).where(Review.customer_id == user_obj.id))
    await db.execute(delete(TechnicianAvailability).where(TechnicianAvailability.technician_id == user_obj.id))
    await db.execute(delete(AuditLog).where(AuditLog.user_id == user_obj.id))
    await db.execute(update(Service).where(Service.customer_id == user_obj.id).values(customer_id=None))
    await db.execute(update(Service).where(Service.assigned_technician_id == user_obj.id).values(assigned_technician_id=None))
    await db.delete(user_obj)
    await db.commit()
    return True
