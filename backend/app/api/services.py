from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate
from app.auth.deps import get_current_user
from app.auth.permissions import require_admin_or_technician
from app.services.service_service import (
    create_public_service_request,
    create_new_service,
    list_services,
    list_services_for_user,
    get_service_detail,
    get_service_by_tracking_code,
    edit_service,
    remove_service,
)

router = APIRouter()

@router.post('/public', response_model=ServiceRead)
async def create_public_service(payload: ServiceCreate, db: AsyncSession = Depends(get_db)):
    try:
        service = await create_public_service_request(db, payload)
        return ServiceRead.model_validate(service)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo agendar el servicio: {exc}",
        ) from exc


@router.get('/public/{tracking_code}', response_model=ServiceRead)
async def get_public_service(tracking_code: str, db: AsyncSession = Depends(get_db)):
    service = await get_service_by_tracking_code(db, tracking_code)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service


@router.post('/', response_model=ServiceRead, dependencies=[Depends(require_admin_or_technician)])
async def create_service(payload: ServiceCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    customer_id = payload.customer_id or current_user.id
    try:
        service = await create_new_service(db, customer_id, payload)
        return ServiceRead.model_validate(service)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo crear el servicio: {exc}",
        ) from exc

@router.get('/', response_model=list[ServiceRead], dependencies=[Depends(require_admin_or_technician)])
async def get_services_endpoint(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    services = await list_services(db, skip, limit)
    return services


@router.get('/me', response_model=list[ServiceRead])
async def get_my_services(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    services = await list_services_for_user(db, current_user.id, current_user.role, skip, limit)
    return services


@router.get('/{service_id}', response_model=ServiceRead, dependencies=[Depends(require_admin_or_technician)])
async def get_service(service_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = await get_service_detail(db, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service


@router.patch('/{service_id}', response_model=ServiceRead, dependencies=[Depends(require_admin_or_technician)])
async def update_service_endpoint(service_id: int, payload: ServiceUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = await get_service_detail(db, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return await edit_service(db, service, payload)


@router.delete('/{service_id}', dependencies=[Depends(require_admin_or_technician)])
async def delete_service_endpoint(service_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = await get_service_detail(db, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    await remove_service(db, service)
    return {"detail": "Service deleted"}
