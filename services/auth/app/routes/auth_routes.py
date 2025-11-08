from fastapi import APIRouter
from ..authentication.service import AuthService
from ..db.models import UserCreate, UserLogin, UserOut, Token

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    return await AuthService.register_user(user.email, user.password)

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    auth_user = await AuthService.authenticate_user(user.email, user.password)
    token = AuthService.create_access_token(subject=auth_user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get('/health')
async def health_check():
    return {'status' : 'auth ok'}