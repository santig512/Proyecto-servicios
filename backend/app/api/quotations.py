from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.deps import get_current_user
from app.schemas.quotation import QuotationCreate, QuotationRead, QuotationUpdate
from app.services.quotation_service import create_new_quotation, list_quotations, get_quotation_detail, edit_quotation, remove_quotation
from app.auth.permissions import require_admin

router = APIRouter()

@router.post('/', response_model=QuotationRead, dependencies=[Depends(require_admin)])
async def create_quotation_endpoint(payload: QuotationCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await create_new_quotation(db, payload)

@router.get('/', response_model=list[QuotationRead])
async def list_quotations_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await list_quotations(db, skip, limit)

@router.get('/{quotation_id}', response_model=QuotationRead)
async def get_quotation_endpoint(quotation_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    quotation = await get_quotation_detail(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
    return quotation

@router.patch('/{quotation_id}', response_model=QuotationRead, dependencies=[Depends(require_admin)])
async def update_quotation_endpoint(quotation_id: int, payload: QuotationUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    quotation = await get_quotation_detail(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
    return await edit_quotation(db, quotation, payload)

@router.delete('/{quotation_id}', dependencies=[Depends(require_admin)])
async def delete_quotation_endpoint(quotation_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    quotation = await get_quotation_detail(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
    await remove_quotation(db, quotation)
    return {"detail": "Quotation deleted"}
