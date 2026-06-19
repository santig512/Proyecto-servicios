from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.deps import get_current_user
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUpdate
from app.services.invoice_service import create_new_invoice, list_invoices, get_invoice_detail, edit_invoice, remove_invoice
from app.auth.permissions import require_admin

router = APIRouter()

@router.post('/', response_model=InvoiceRead, dependencies=[Depends(require_admin)])
async def create_invoice_endpoint(payload: InvoiceCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await create_new_invoice(db, payload)

@router.get('/', response_model=list[InvoiceRead])
async def list_invoices_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await list_invoices(db, skip, limit)

@router.get('/{invoice_id}', response_model=InvoiceRead)
async def get_invoice_endpoint(invoice_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    invoice = await get_invoice_detail(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice

@router.patch('/{invoice_id}', response_model=InvoiceRead, dependencies=[Depends(require_admin)])
async def update_invoice_endpoint(invoice_id: int, payload: InvoiceUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    invoice = await get_invoice_detail(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return await edit_invoice(db, invoice, payload)

@router.delete('/{invoice_id}', dependencies=[Depends(require_admin)])
async def delete_invoice_endpoint(invoice_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    invoice = await get_invoice_detail(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    await remove_invoice(db, invoice)
    return {"detail": "Invoice deleted"}
