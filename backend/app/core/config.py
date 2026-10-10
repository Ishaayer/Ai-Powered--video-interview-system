from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()



API_V1_PREFIX: str = "/api/v1"

PROJECT_NAME: str = "AI-Powered Intelligent Video Interview Assessment"

PROJECT_VERSION: str = "1.0.0"

PROJECT_DESCRIPTION: str = (
    "AI-Powered Intelligent Video Interview Assessment System"
)