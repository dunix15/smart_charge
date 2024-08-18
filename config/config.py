from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    platform: str = "darwin_arm64"
    ps_id: str = ""
    charging_state_file: str = "data/charging_state.json"
    tesla_vin: str = ""
    tesla_key_name: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
