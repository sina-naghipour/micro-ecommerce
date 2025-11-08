from sqlalchemy.ext.asyncio import AsyncSession
from .repository import ProfileRepository
from .models import ProfileCreate

class ProfileService:
    @staticmethod
    async def create_profile(db: AsyncSession, profile: ProfileCreate):
        existing = await ProfileRepository.get_by_email(db, profile.email)
        if existing:
            raise ValueError("Profile already exists")
        return await ProfileRepository.create_profile(db, profile.model_dump())

    @staticmethod
    async def list_profiles(db: AsyncSession):
        return await ProfileRepository.list_profiles(db)

    @staticmethod
    async def get_profile(db: AsyncSession, profile_id: int):
        profile = await ProfileRepository.get_by_id(db, profile_id)
        if not profile:
            raise ValueError("Profile not found")
        return profile
