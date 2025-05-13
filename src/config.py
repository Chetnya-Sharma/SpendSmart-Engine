import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    jwt_secret: str
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')

settings = Settings()
