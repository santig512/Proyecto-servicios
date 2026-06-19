from app.models.payment import Payment
from app.repositories.payment_repository import create_payment, get_payments, get_payment_by_id, update_payment, delete_payment

async def create_new_payment(db, payment_in):
    payment = Payment(
        invoice_id=payment_in.invoice_id,
        transaction_reference=payment_in.transaction_reference,
        amount=payment_in.amount,
        status=payment_in.status,
        provider=payment_in.provider,
    )
    return await create_payment(db, payment)

async def list_payments(db, skip: int = 0, limit: int = 100):
    return await get_payments(db, skip, limit)

async def get_payment_detail(db, payment_id: int):
    return await get_payment_by_id(db, payment_id)

async def edit_payment(db, payment, payment_in):
    payload = payment_in.model_dump(exclude_unset=True)
    return await update_payment(db, payment, payload)

async def remove_payment(db, payment):
    return await delete_payment(db, payment)
