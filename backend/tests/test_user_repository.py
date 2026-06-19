import pytest
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user,
    get_users,
    update_user,
    delete_user,
)


@pytest.mark.asyncio
async def test_user_repository_crud(db):
    user = User(first_name="Test", last_name="User", email="test@example.com", password_hash="hash")
    created = await create_user(db, user)
    assert created.id is not None

    fetched = await get_user_by_email(db, "test@example.com")
    assert fetched.email == "test@example.com"

    fetched2 = await get_user(db, created.id)
    assert fetched2.id == created.id

    users = await get_users(db)
    assert len(users) == 1

    updated = await update_user(db, created, {"first_name": "Updated"})
    assert updated.first_name == "Updated"

    ok = await delete_user(db, created)
    assert ok is True

    users = await get_users(db)
    assert users == []
