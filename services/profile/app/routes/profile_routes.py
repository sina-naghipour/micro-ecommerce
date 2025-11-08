from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.models import Profile, ProfileCreate, ProfileOut
from ..db.db import get_db
from ..authentication.auth import verify_token

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "profile ok"}

@router.post("/", response_model=ProfileOut, dependencies=[Depends(verify_token)])
async def create_profile(profile: ProfileCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).where(Profile.email == profile.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    new_profile = Profile(**profile.model_dump())
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile



@router.get("/", response_model=list[ProfileOut], dependencies=[Depends(verify_token)])
async def list_profiles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile))
    return result.scalars().all()

@router.get("/{profile_id}", response_model=ProfileOut, dependencies=[Depends(verify_token)])
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

