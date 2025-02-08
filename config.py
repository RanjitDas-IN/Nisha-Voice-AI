from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    #API KEY OF TYPE CAST API
    TYPECAST_API_KEY: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
    )

settings = Settings()