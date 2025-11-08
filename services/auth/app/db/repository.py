from sqlalchemy.future import select
from .db import AsyncSessionLocal
from .models import User
from fastapi import HTTPException, status

class UserRepository:
    @staticmethod
    async def get_by_email(email: str):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalars().first()

    @staticmethod
    async def create_user(email: str, password_hash: str):
        async with AsyncSessionLocal() as session:
            user = User(email=email, password_hash=password_hash)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def list_users():
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User))
            return result.scalars().all()
