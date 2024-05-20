from pydantic import BaseModel


class InverterData(BaseModel):
    battery_level_percent: float
    charging_discharging_power: float
    load_power: float
    power_grid_power: float
    pv_power: float
