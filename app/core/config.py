from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ИС агентства недвижимости (MVP паттернов)"
    database_url: str = "postgresql+psycopg://realty:realty@localhost:5433/realty"


settings = Settings()
