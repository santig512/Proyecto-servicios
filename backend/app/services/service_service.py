from app.repositories.service_repository import (
    create_service,
    get_services,
    get_services_for_user,
    get_service_by_id,
    get_service_by_tracking_code as repo_get_service_by_tracking_code,
    update_service,
    delete_service,
)
from app.models.service import Service
from app.repositories.user_repository import get_user_by_email
from app.services.notification_service import notify_non_admin_users
from uuid import uuid4
from datetime import timezone


def _normalize_scheduled_date(scheduled_date):
    if scheduled_date and scheduled_date.tzinfo is not None:
        return scheduled_date.astimezone(timezone.utc).replace(tzinfo=None)
    return scheduled_date

async def create_public_service_request(db, service_in):
    linked_user = None
    if service_in.customer_email:
        linked_user = await get_user_by_email(db, service_in.customer_email)

    service = Service(
        customer_id=service_in.customer_id or (linked_user.id if linked_user else None),
        customer_name=service_in.customer_name,
        customer_email=service_in.customer_email,
        customer_phone=service_in.customer_phone,
        service_address=service_in.service_address,
        postal_code=service_in.postal_code,
        tracking_code=uuid4().hex[:10].upper(),
        title=service_in.title,
        description=service_in.description,
        category_id=service_in.category_id,
        address_id=service_in.address_id,
        scheduled_date=_normalize_scheduled_date(service_in.scheduled_date),
        estimated_cost=service_in.estimated_cost,
        status="pending",
        priority="normal",
    )
    service = await create_service(db, service)
    try:
        await notify_non_admin_users(
            db,
            title='Nuevo servicio agendado',
            body=f'Se registró un nuevo servicio: {service.title} ({service.tracking_code}).',
        )
    except Exception:
        pass
    return service


async def create_new_service(db, customer_id: int, service_in):
    service = Service(
        customer_id=customer_id,
        customer_name=service_in.customer_name,
        customer_email=service_in.customer_email,
        customer_phone=service_in.customer_phone,
        service_address=service_in.service_address,
        postal_code=service_in.postal_code,
        tracking_code=uuid4().hex[:10].upper(),
        title=service_in.title,
        description=service_in.description,
        category_id=service_in.category_id,
        address_id=service_in.address_id,
        scheduled_date=_normalize_scheduled_date(service_in.scheduled_date),
        estimated_cost=service_in.estimated_cost,
        status="pending",
        priority="normal",
    )
    service = await create_service(db, service)
    try:
        await notify_non_admin_users(
            db,
            title='Nuevo servicio agendado',
            body=f'Se registró un nuevo servicio: {service.title} ({service.tracking_code}).',
        )
    except Exception:
        pass
    return service

async def list_services(db, skip: int = 0, limit: int = 100):
    return await get_services(db, skip, limit)


async def list_services_for_user(db, user_id: int, role: str, skip: int = 0, limit: int = 100):
    if role in ("admin", "technician"):
        return await get_services(db, skip, limit)
    return await get_services_for_user(db, user_id, role, skip, limit)


async def get_service_detail(db, service_id: int):
    return await get_service_by_id(db, service_id)


async def get_service_by_tracking_code(db, tracking_code: str):
    return await repo_get_service_by_tracking_code(db, tracking_code)


async def edit_service(db, service: Service, service_in):
    payload = service_in.model_dump(exclude_unset=True)
    if "scheduled_date" in payload:
        payload["scheduled_date"] = _normalize_scheduled_date(payload["scheduled_date"])
    return await update_service(db, service, payload)


async def remove_service(db, service: Service):
    return await delete_service(db, service)
