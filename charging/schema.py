from pydantic import BaseModel

from inverter.schema import InverterData


class ChargingState(BaseModel):
    inverter_data: InverterData | None
    amps: int
    is_charging: bool
    is_active: bool
    use_battery: bool
