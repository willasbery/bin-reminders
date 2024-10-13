
from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated, Any, Literal


def parse_cors(value: Any) -> list[AnyUrl] | str:
    if isinstance(value, str) and not value.startswith("["):
        return [i.strip() for i in value.split(",")]
    elif isinstance(value, list | str):
        return value
    return ValueError(value)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["development", "production"] = "development"
    
    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "development":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"
    
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
    
    PROJECT_NAME: str = "Bin Collection API"
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}"
    
    
settings = Settings()