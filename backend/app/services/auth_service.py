from app.repositories.user_repository import get_user_by_email, create_user
from app.auth.utils import hash_password, verify_password, create_access_token
from app.models.user import User

async def register_user(db, user_in):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        return None
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        phone=user_in.phone,
        password_hash=hash_password(user_in.password),
        role=user_in.role or "customer",
    )
    return await create_user(db, user)

async def authenticate_user(db, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "user": user}
