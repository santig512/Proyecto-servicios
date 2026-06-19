from sqlalchemy import select, delete, update
from app.models.service import Service
from app.models.chat_room import ChatRoom
from app.models.review import Review
from app.models.quotation import Quotation
from app.models.service_image import ServiceImage
from app.models.invoice import Invoice

async def create_service(db, service_obj):
    db.add(service_obj)
    await db.commit()
    await db.refresh(service_obj)
    return service_obj

async def get_services(db, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Service).offset(skip).limit(limit))
    return result.scalars().all()


async def get_services_for_user(db, user_id: int, role: str, skip: int = 0, limit: int = 100):
    query = select(Service)
    if role == 'customer':
        from app.repositories.user_repository import get_user
        user = await get_user(db, user_id)
        query = query.where((Service.customer_id == user_id) | (Service.customer_email == user.email))
    elif role == 'technician':
        query = query.where(Service.assigned_technician_id == user_id)

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_service_by_id(db, service_id: int):
    result = await db.execute(select(Service).where(Service.id == service_id))
    return result.scalars().first()


async def get_service_by_tracking_code(db, tracking_code: str):
    result = await db.execute(select(Service).where(Service.tracking_code == tracking_code))
    return result.scalars().first()


async def update_service(db, service_obj: Service, updates: dict):
    for field, value in updates.items():
        setattr(service_obj, field, value)
    await db.commit()
    await db.refresh(service_obj)
    return service_obj


async def delete_service(db, service_obj: Service):
    await db.execute(delete(ChatRoom).where(ChatRoom.service_id == service_obj.id))
    await db.execute(delete(Review).where(Review.service_id == service_obj.id))
    await db.execute(delete(Quotation).where(Quotation.service_id == service_obj.id))
    await db.execute(delete(ServiceImage).where(ServiceImage.service_id == service_obj.id))
    await db.execute(delete(Invoice).where(Invoice.service_id == service_obj.id))
    await db.execute(update(Service).where(Service.id == service_obj.id).values(customer_id=None, assigned_technician_id=None))
    await db.delete(service_obj)
    await db.commit()
