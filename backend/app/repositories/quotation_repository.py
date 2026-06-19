from sqlalchemy import select
from app.models.quotation import Quotation

async def create_quotation(db, quotation_obj):
    db.add(quotation_obj)
    await db.commit()
    await db.refresh(quotation_obj)
    return quotation_obj

async def get_quotations(db, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Quotation).offset(skip).limit(limit))
    return result.scalars().all()

async def get_quotation_by_id(db, quotation_id: int):
    result = await db.execute(select(Quotation).where(Quotation.id == quotation_id))
    return result.scalars().first()

async def update_quotation(db, quotation_obj: Quotation, updates: dict):
    for field, value in updates.items():
        setattr(quotation_obj, field, value)
    await db.commit()
    await db.refresh(quotation_obj)
    return quotation_obj

async def delete_quotation(db, quotation_obj: Quotation):
    await db.delete(quotation_obj)
    await db.commit()
