from functools import lru_cache

from pydantic import Extra
from pydantic_settings import BaseSettings


class TemplateSettings(BaseSettings):
    blocks_templates_folder: str

    class Config:
        env_file = ".env"
        extra = Extra.allow


@lru_cache
def get_template_settings() -> TemplateSettings:
    return TemplateSettings()
