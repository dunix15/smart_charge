from pydantic import BaseModel


class InverterData(BaseModel):
    production_kw: float
    net_import_kw: float
    consumption_kw: float
    battery_discharge_kw: float
    battery_soc: float
