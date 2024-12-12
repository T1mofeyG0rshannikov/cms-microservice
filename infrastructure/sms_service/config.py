import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class SMSAeroConfig(BaseSettings):
    sms_api_key: str = os.getenv("SMS_API_KEY")
    sms_email: str = os.getenv("SMS_EMAIL")


@lru_cache
def get_sms_config() -> SMSAeroConfig:
    return SMSAeroConfig()
