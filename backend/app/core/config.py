import platform

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "servicios_db"
    REDIS_URL: str = "redis://redis:6379/0"
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    S3_BUCKET: str | None = None

    model_config = SettingsConfigDict(env_file=".env")

    def postgres_host(self) -> str:
        if self.POSTGRES_HOST:
            return self.POSTGRES_HOST
        return "localhost" if platform.system().lower().startswith("win") else "db"

settings = Settings()
