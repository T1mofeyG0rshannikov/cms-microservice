import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class JwtSettings(BaseSettings):
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    expires_in: str = os.getenv("EXPIRES_IN")


@lru_cache
def get_jwt_settings() -> JwtSettings:
    return JwtSettings()
