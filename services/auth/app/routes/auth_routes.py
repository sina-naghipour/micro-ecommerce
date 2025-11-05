from fastapi import APIRouter
from ..db.models import UserCreate, UserLogin, UserOut, Token
from ..authentication import auth


router = APIRouter()


@router.post('/register', response_model=UserOut)
async def register(user: UserCreate):
    user_response = await auth.create_user(user.email, user.password)
    return user_response


@router.post('/login', response_model=Token)
async def login(user: UserLogin):
    authenticated_user = await auth.authenticate_user(user.email, user.password)
    token = auth.create_access_token(subject=user.email)
    return {'access_token' : token, 'token_type' : 'bearer'}


@router.get('/health')
async def health_check():
    return {'status' : 'auth ok'}