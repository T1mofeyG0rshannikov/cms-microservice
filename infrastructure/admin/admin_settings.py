from functools import lru_cache

from pydantic import Extra
from pydantic_settings import BaseSettings


class AdminSettings(BaseSettings):
    admin_domain: str
    admin_url: str

    class Config:
        env_file = ".env"
        extra = Extra.allow


@lru_cache
def get_admin_settings() -> AdminSettings:
    return AdminSettings()
