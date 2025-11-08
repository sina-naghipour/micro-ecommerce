import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta, timezone
from ..db.db import AsyncSessionLocal
from fastapi import HTTPException, status
from sqlalchemy.future import select
from ..db.models import User

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


JWT_SECRET = os.getenv("JWT_SECRET", "random-security-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str)-> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {'token' : subject, 'exp' : expire}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired.')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token.')

async def create_user(email: str, password: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail      = 'Email already registered.'
            )
            
        user = User(email=email, password_hash=hash_password(password))
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def authenticate_user(email: str, password:str):
    async with AsyncSessionLocal() as session:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()
        
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail      = 'Invalid credentials'
            )
            
        return user