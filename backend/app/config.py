from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    use_demo_data: bool = True
    database_url: str = "sqlite:///./app/data/shelfie.db"
    google_books_api_key: str = ""
    tesseract_cmd: str = "tesseract"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
