import pytest
from app.models.user import User
from app.models.service import Service
from app.repositories.service_repository import (
    create_service,
    get_services,
    get_service_by_id,
    update_service,
    delete_service,
)


@pytest.mark.asyncio
async def test_service_repository_crud(db):
    user = User(first_name="Cust", email="cust@example.com", password_hash="h")
    db.add(user)
    await db.commit()
    await db.refresh(user)

    service = Service(customer_id=user.id, title="Fix AC", description="AC broken")
    created = await create_service(db, service)
    assert created.id is not None

    fetched = await get_service_by_id(db, created.id)
    assert fetched.title == "Fix AC"

    services = await get_services(db)
    assert len(services) == 1

    updated = await update_service(db, created, {"status": "in_progress"})
    assert updated.status == "in_progress"

    await delete_service(db, created)
    services = await get_services(db)
    assert services == []
