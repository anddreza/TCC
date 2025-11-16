from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    allow_origin: Optional[str] = None
    
