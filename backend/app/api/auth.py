from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.schemas.user import UserCreate, UserRead
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import register_user, authenticate_user
from app.auth.utils import decode_token, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post('/register', response_model=UserRead)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user

@router.post('/login', response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await authenticate_user(db, payload.email, payload.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": result['access_token'], "token_type": "bearer", "user": result['user']}


@router.post('/refresh', response_model=Token)
async def refresh(token: Token, db: AsyncSession = Depends(get_db)):
    payload = decode_token(token.access_token)
    if not payload or 'sub' not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    new_token = create_access_token(subject=payload['sub'], expires_delta=timedelta(minutes=60))
    return {"access_token": new_token, "token_type": "bearer"}


@router.post('/logout')
async def logout():
    # For stateless JWT, logout is handled client-side or via token revocation list (not implemented)
    return {"detail": "logout successful (client should discard token)"}
