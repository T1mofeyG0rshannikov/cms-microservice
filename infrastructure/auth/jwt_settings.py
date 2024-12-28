from functools import lru_cache

from pydantic import Extra
from pydantic_settings import BaseSettings


class JwtSettings(BaseSettings):
    secret_key: str
    algorithm: str
    expires_in: int

    class Config:
        env_file = ".env"
        extra = Extra.allow


@lru_cache
def get_jwt_settings() -> JwtSettings:
    return JwtSettings()
