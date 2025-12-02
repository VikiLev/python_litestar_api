from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_NAME: str = "offersAdmin"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    
    DB_URL: str | None = None
    
    DEBUG: bool = True
    SECRET_KEY: str  # Обов'язковий параметр без дефолту

    class Config:
        env_file = ".env"
        extra = "ignore"
    
    @property
    def database_url(self) -> str:
        if self.DB_URL:
            return self.DB_URL
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
