from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.permissions import require_admin
from app.auth.utils import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.repositories.user_repository import create_user, get_users, get_user, update_user, delete_user

router = APIRouter()

@router.post('/', response_model=UserRead, dependencies=[Depends(require_admin)])
async def create_user_admin(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    user = await create_user(db, user)
    return user

@router.get('/', response_model=list[UserRead], dependencies=[Depends(require_admin)])
async def list_users_admin(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_users(db, skip, limit)

@router.get('/{user_id}', response_model=UserRead, dependencies=[Depends(require_admin)])
async def get_user_admin(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

@router.patch('/{user_id}', response_model=UserRead, dependencies=[Depends(require_admin)])
async def update_user_admin(user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    data = payload.model_dump(exclude_unset=True)
    return await update_user(db, user, data)

@router.delete('/{user_id}', dependencies=[Depends(require_admin)])
async def delete_user_admin(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    await delete_user(db, user)
    return {'detail': 'User deleted'}
