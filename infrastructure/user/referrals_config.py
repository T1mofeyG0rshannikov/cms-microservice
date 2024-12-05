import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class ReferralConfig(BaseSettings):
    total_referral_level: int = os.getenv("TOTAL_REFERRAL_LEVEL")


@lru_cache
def get_referral_config() -> ReferralConfig:
    return ReferralConfig()
