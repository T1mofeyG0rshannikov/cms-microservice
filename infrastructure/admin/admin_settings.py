from functools import lru_cache
from typing import Annotated

from pydantic import Extra, field_validator
from pydantic_settings import BaseSettings, NoDecode


class AdminSettings(BaseSettings):
    admin_domain: str
    valid_admin_urls: Annotated[list[str], NoDecode]
    admin_url: str

    class Config:
        env_file = ".env"
        extra = Extra.allow

    @field_validator("valid_admin_urls", mode="before")
    @classmethod
    def decode_numbers(cls, v: str) -> list[str]:
        return [x for x in v.split(",")]


@lru_cache
def get_admin_settings() -> AdminSettings:
    return AdminSettings()
