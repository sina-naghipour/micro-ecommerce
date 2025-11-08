from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET:                  str = 'random-security-secret'
    JWT_ALGORITHM:               str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS:   int = 30
    DB_URL:                      str = 'postgresql+asyncpg://postgres:toor@db_auth:5432/ecommerce_auth'
    
    class Config:
        env_file = '.env'

settings = Settings()