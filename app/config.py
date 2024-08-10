from fastapi import FastAPI
from pydantic_settings import BaseSettings  # Updated import for Pydantic v2

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"  # You can specify the environment file if needed

settings = Settings()  # Instantiating settings

