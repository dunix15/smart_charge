from pydantic import BaseModel, computed_field

from inverter.schema import InverterData


class ChargingState(BaseModel):
    inverter_data: InverterData
    amps: int = 0
    is_charging: bool = False
    is_active: bool = False
    use_battery: bool = True
    inverter_max_power_kw: float = 9.5
    battery_max_power_kw: float = 3.0
    battery_min_soc: float = 0.3
    voltage: float = 245.0

    @computed_field
    @property
    def available_power_kw(self) -> float:
        inverter_data = self.inverter_data
        available_max_power_kw = inverter_data.production_kw
        if self.use_battery and inverter_data.battery_soc > self.battery_min_soc:
            available_max_power_kw += self.battery_max_power_kw

        available_max_power_kw = min(available_max_power_kw, self.inverter_max_power_kw)

        net_consumption_kw = max(inverter_data.consumption_kw - self.amps * self.voltage * 3 / 1000, 0)

        available_power_kw = available_max_power_kw - net_consumption_kw

        return available_power_kw
