from sqlalchemy.ext.asyncio import AsyncSession
from .models import Profile

class ProfileRepository:
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        result = await db.execute(Profile.__table__.select().where(Profile.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(db: AsyncSession, profile_id: int):
        result = await db.execute(Profile.__table__.select().where(Profile.id == profile_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_profiles(db: AsyncSession):
        result = await db.execute(Profile.__table__.select())
        return result.scalars().all()

    @staticmethod
    async def create_profile(db: AsyncSession, profile_data: dict):
        profile = Profile(**profile_data)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile
