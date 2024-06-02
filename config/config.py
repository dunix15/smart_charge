from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    platform: str = "darwin_arm64"
    ps_id: str = ""
    inverter_max_power_kw: float = 9.5
    battery_max_power_kw: float = 3.0
    battery_min_soc: float = 0.3
    voltage: float = 245.0
    charging_state_file: str = "data/charging_state.json"
    tesla_vin: str = ""
    tesla_key_name: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
