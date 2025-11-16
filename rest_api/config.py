from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    allow_origin: Optional[str] = None
    mongo_uri: Optional[str] = None
    google_api_key: Optional[str] = None
