import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class TemplateSettings(BaseSettings):
    blocks_templates_folder: str = os.getenv("BLOCKS_TEMPLATES_FOLDER")


@lru_cache
def get_template_settings() -> TemplateSettings:
    return TemplateSettings()
