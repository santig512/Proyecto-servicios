from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.deps import get_current_user
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate
from app.services.payment_service import create_new_payment, list_payments, get_payment_detail, edit_payment, remove_payment
from app.auth.permissions import require_admin
from fastapi import Request
from app.services.payment_provider import handle_webhook

router = APIRouter()

@router.post('/', response_model=PaymentRead, dependencies=[Depends(require_admin)])
async def create_payment_endpoint(payload: PaymentCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await create_new_payment(db, payload)

@router.get('/', response_model=list[PaymentRead])
async def list_payments_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await list_payments(db, skip, limit)

@router.get('/{payment_id}', response_model=PaymentRead)
async def get_payment_endpoint(payment_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    payment = await get_payment_detail(db, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment

@router.patch('/{payment_id}', response_model=PaymentRead, dependencies=[Depends(require_admin)])
async def update_payment_endpoint(payment_id: int, payload: PaymentUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    payment = await get_payment_detail(db, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return await edit_payment(db, payment, payload)

@router.delete('/{payment_id}', dependencies=[Depends(require_admin)])
async def delete_payment_endpoint(payment_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    payment = await get_payment_detail(db, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    await remove_payment(db, payment)
    return {"detail": "Payment deleted"}


@router.post('/webhook')
async def payments_webhook(request: Request):
    payload = await request.json()
    event = handle_webhook(payload)
    # In a real integration, validate signatures, find invoice and update payment status
    return {"received": True, "event": event}
