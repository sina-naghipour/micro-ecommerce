from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db
from app.db.service import ProfileService
from app.db.models import ProfileCreate, ProfileOut
from app.authentication.auth import verify_token

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "profile ok"}

@router.post("/", response_model=ProfileOut, dependencies=[Depends(verify_token)])
async def create_profile(profile: ProfileCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await ProfileService.create_profile(db, profile)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ProfileOut], dependencies=[Depends(verify_token)])
async def list_profiles(db: AsyncSession = Depends(get_db)):
    return await ProfileService.list_profiles(db)

@router.get("/{profile_id}", response_model=ProfileOut, dependencies=[Depends(verify_token)])
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await ProfileService.get_profile(db, profile_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
