from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str = "dev-secret"
    JWT_ALGORITHM: str = "HS256"
    REDIS_URL: str = "redis://cart_redis:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()
