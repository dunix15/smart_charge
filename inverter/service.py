import json
import subprocess

from config.config import settings
from inverter.schema import InverterData


class InverterService:
    @staticmethod
    def run_command() -> str:
        result = subprocess.run(
            [
                f"./bin/{settings.platform}/GoSungrow",
                "api",
                "get",
                "getPsDetailWithPsType",
                f'{{"ps_id":"{settings.ps_id}"}}',
            ],
            capture_output=True,
            text=True,
        )
        result.check_returncode()  # This will raise an error if the command failed
        return result.stdout

    @staticmethod
    def parse_output(output: str) -> InverterData:
        data = json.loads(output)
        inverter_data = InverterData(
            production_kw=data["pv_power_map"]["value"],
            net_import_kw=data["power_grid_power_map"]["value"],
            consumption_kw=data["load_power_map"]["value"],
            battery_discharge_kw=data["charging_discharging_power_map"]["value"],
            battery_soc=data["battery_level_percent"] / 100,
        )
        return inverter_data

    def fetch_data(self) -> InverterData:
        output = self.run_command()
        inverter_data = self.parse_output(output)
        return inverter_data
