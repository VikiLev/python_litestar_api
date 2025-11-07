from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_NAME: str = "offersAdmin"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/offersAdmin"

    DEBUG: bool = True
    SECRET_KEY: str = "secret_key_qoihrw1892351o5ui9y887qrfhn23oiurh298h932u"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
