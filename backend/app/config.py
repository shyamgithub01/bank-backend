from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        # Loads .env at project root by default:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # If your .env lives under `app/`, uncomment the next line:
        # env_file = "app/.env"

settings = Settings()