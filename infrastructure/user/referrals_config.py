from functools import lru_cache

from pydantic import Extra
from pydantic_settings import BaseSettings


class ReferralConfig(BaseSettings):
    total_referral_level: int

    class Config:
        env_file = ".env"
        extra = Extra.allow


@lru_cache
def get_referral_config() -> ReferralConfig:
    return ReferralConfig()
