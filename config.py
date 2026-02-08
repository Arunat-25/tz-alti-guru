from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

ENV_PATH = BASE_DIR / ".env_test"  # заменить на .env_test для тестов


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=ENV_PATH)


settings = Settings()


if __name__ == "__main__":
    print(f"Host: {settings.POSTGRES_HOST}")
    print(f"Port: {settings.POSTGRES_PORT}")
    print(f"User: {settings.POSTGRES_USER}")
    print(f"Password: {settings.POSTGRES_PASSWORD}")
    print(f"Database: {settings.POSTGRES_DB}")
    print(f"URL: {settings.DATABASE_URL}")
