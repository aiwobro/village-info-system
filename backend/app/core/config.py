import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY: str = "dev_secret_key_for_village_info_system_2024"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    PROJECT_NAME: str = "VillageInfoSystem"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def db_url(self) -> str:
        return self.DATABASE_URL


settings = Settings()
