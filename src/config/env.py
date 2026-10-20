from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar


class Env(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=".env")

    google_api_key: str = ""
    google_project_id: str = ""

env_variables = Env()
