from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    platform_base_url: str = "https://api.23bisnis.com"
    addon_slug: str = "my-addon"
    client_secret: str = "replace-me"
    db_url: str = "sqlite:///./addon.db"


settings = Settings()
