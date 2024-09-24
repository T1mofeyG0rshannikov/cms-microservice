import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AdminSettings(BaseSettings):
    admin_domain: str = os.getenv("ADMIN_DOMAIN")
    admin_url: str = os.getenv("ADMIN_URL")


@lru_cache
def get_admin_settings() -> AdminSettings:
    return AdminSettings()
