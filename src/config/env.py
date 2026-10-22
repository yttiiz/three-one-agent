from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar


class Env(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=".env")

    google_api_key: str = ""
    tavily_api_key: str = ""
    memory_path: str = ""


env_variables = Env()
