from pydantic import BaseModel


class InverterData(BaseModel):
    """
    Schema compatible with charge hq push API
    https://chargehq.net/kb/push-api
    """
    production_kw: float
    net_import_kw: float
    consumption_kw: float
    battery_discharge_kw: float
    battery_soc: float
