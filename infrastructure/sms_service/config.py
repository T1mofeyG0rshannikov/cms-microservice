from functools import lru_cache

from pydantic import Extra
from pydantic_settings import BaseSettings


class SMSAeroConfig(BaseSettings):
    sms_api_key: str
    sms_email: str

    class Config:
        env_file = ".env"
        extra = Extra.allow


@lru_cache
def get_sms_config() -> SMSAeroConfig:
    return SMSAeroConfig()
