import pytest

from app.schemas.service import ServiceCreate
from app.services.service_service import create_public_service_request, get_service_by_tracking_code


@pytest.mark.asyncio
async def test_public_service_request_creates_tracking_code(db):
    payload = ServiceCreate(
        title='Reparación de aire acondicionado',
        description='No enfría correctamente',
        customer_name='Cliente Público',
        customer_email='cliente@example.com',
        customer_phone='555-1234',
        service_address='Calle 123',
        postal_code='33101',
    )

    service = await create_public_service_request(db, payload)

    assert service.id is not None
    assert service.tracking_code
    assert service.status == 'pending'
    assert service.customer_name == 'Cliente Público'
    assert service.postal_code == '33101'

    fetched = await get_service_by_tracking_code(db, service.tracking_code)
    assert fetched is not None
    assert fetched.id == service.id
    assert fetched.postal_code == '33101'
