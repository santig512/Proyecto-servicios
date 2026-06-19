from sqlalchemy import select
from app.models.payment import Payment

async def create_payment(db, payment_obj):
    db.add(payment_obj)
    await db.commit()
    await db.refresh(payment_obj)
    return payment_obj

async def get_payments(db, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Payment).offset(skip).limit(limit))
    return result.scalars().all()

async def get_payment_by_id(db, payment_id: int):
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    return result.scalars().first()

async def update_payment(db, payment_obj: Payment, updates: dict):
    for field, value in updates.items():
        setattr(payment_obj, field, value)
    await db.commit()
    await db.refresh(payment_obj)
    return payment_obj

async def delete_payment(db, payment_obj: Payment):
    await db.delete(payment_obj)
    await db.commit()
