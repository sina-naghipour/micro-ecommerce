from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from fastapi import HTTPException, status
from ..db.repository import UserRepository
from ..core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return pwd_context.verify(password, hashed)

    @staticmethod
    def create_access_token(subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    async def register_user(email: str, password: str):
        existing = await UserRepository.get_by_email(email)
        if existing:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")
        hashed = AuthService.hash_password(password)
        return await UserRepository.create_user(email=email, password_hash=hashed)

    @staticmethod
    async def authenticate_user(email: str, password: str):
        user = await UserRepository.get_by_email(email)
        if not user or not AuthService.verify_password(password, user.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        return user
