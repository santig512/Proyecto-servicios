from app.models.invoice import Invoice
from app.repositories.invoice_repository import create_invoice, get_invoices, get_invoice_by_id, update_invoice, delete_invoice

async def create_new_invoice(db, invoice_in):
    invoice = Invoice(
        service_id=invoice_in.service_id,
        invoice_number=invoice_in.invoice_number,
        amount=invoice_in.amount,
        payment_status=invoice_in.payment_status,
        payment_method=invoice_in.payment_method,
    )
    return await create_invoice(db, invoice)

async def list_invoices(db, skip: int = 0, limit: int = 100):
    return await get_invoices(db, skip, limit)

async def get_invoice_detail(db, invoice_id: int):
    return await get_invoice_by_id(db, invoice_id)

async def edit_invoice(db, invoice, invoice_in):
    payload = invoice_in.model_dump(exclude_unset=True)
    return await update_invoice(db, invoice, payload)

async def remove_invoice(db, invoice):
    return await delete_invoice(db, invoice)
