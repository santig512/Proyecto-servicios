from app.models.quotation import Quotation
from app.repositories.quotation_repository import create_quotation, get_quotations, get_quotation_by_id, update_quotation, delete_quotation

async def create_new_quotation(db, quotation_in):
    quotation = Quotation(
        service_id=quotation_in.service_id,
        amount=quotation_in.amount,
        description=quotation_in.description,
    )
    return await create_quotation(db, quotation)

async def list_quotations(db, skip: int = 0, limit: int = 100):
    return await get_quotations(db, skip, limit)

async def get_quotation_detail(db, quotation_id: int):
    return await get_quotation_by_id(db, quotation_id)

async def edit_quotation(db, quotation, quotation_in):
    payload = quotation_in.model_dump(exclude_unset=True)
    return await update_quotation(db, quotation, payload)

async def remove_quotation(db, quotation):
    return await delete_quotation(db, quotation)
