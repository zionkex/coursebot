from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    postgres_port: int = 5432
    echo: bool = False
    max_overflow: int = 10

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


class RedisConfig(BaseModel):
    host: str
    port: int = 6379
    db: int = 0
    password: str | None = None

    @property
    def url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )
    db: DatabaseConfig
    redis: RedisConfig
    BOT_TOKEN: str


settings = Settings()

print("DATABASE URL:", settings.db.url)
print("REDIS URL:", settings.redis.url)
