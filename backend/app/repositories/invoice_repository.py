from sqlalchemy import select
from app.models.invoice import Invoice

async def create_invoice(db, invoice_obj):
    db.add(invoice_obj)
    await db.commit()
    await db.refresh(invoice_obj)
    return invoice_obj

async def get_invoices(db, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Invoice).offset(skip).limit(limit))
    return result.scalars().all()

async def get_invoice_by_id(db, invoice_id: int):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    return result.scalars().first()

async def update_invoice(db, invoice_obj: Invoice, updates: dict):
    for field, value in updates.items():
        setattr(invoice_obj, field, value)
    await db.commit()
    await db.refresh(invoice_obj)
    return invoice_obj

async def delete_invoice(db, invoice_obj: Invoice):
    await db.delete(invoice_obj)
    await db.commit()
