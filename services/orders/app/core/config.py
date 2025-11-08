from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str = "dev-secret"
    JWT_ALGORITHM: str = "HS256"
    MONGO_URL: str = "mongodb://mongo_orders:27017"
    DATABASE_NAME: str = "ecommerce_orders"

    class Config:
        env_file = ".env"

settings = Settings()
