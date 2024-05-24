from pydantic import BaseModel

from inverter.schema import InverterData


class ChargingState(BaseModel):
    inverter_data: InverterData | None
    amps: int
    is_active: bool
