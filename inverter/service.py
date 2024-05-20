import json
import subprocess
from datetime import datetime, timezone
from typing import List, Dict

from config.config import settings
from inverter.schema import InverterData


class InverterService:
    def __init__(self):
        self.data_history: List[Dict[str, InverterData]] = []

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
            battery_level_percent=data["battery_level_percent"],
            charging_discharging_power=data["charging_discharging_power_map"]["value"],
            load_power=data["load_power_map"]["value"],
            power_grid_power=data["power_grid_power_map"]["value"],
            pv_power=data["pv_power_map"]["value"],
        )
        return inverter_data

    def store_data(self, data: InverterData):
        timestamp = datetime.now(timezone.utc).isoformat()
        self.data_history.append({timestamp: data})

    def fetch_data(self) -> InverterData:
        output = self.run_command()
        inverter_data = self.parse_output(output)
        self.store_data(inverter_data)
        return inverter_data
