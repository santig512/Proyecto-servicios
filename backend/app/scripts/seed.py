import asyncio
from app.database.session import AsyncSessionLocal, engine
from app.models.user import User
from app.auth.utils import hash_password

async def create_admin():
    async with AsyncSessionLocal() as session:
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password_hash=hash_password('admin123'),
            role='admin'
        )
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        print('Admin user created:', admin.email)

if __name__ == '__main__':
    asyncio.run(create_admin())
