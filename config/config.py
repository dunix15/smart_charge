from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    platform: str = "darwin_arm64"
    ps_id: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
