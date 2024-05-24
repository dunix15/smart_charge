import json
import logging
import subprocess
from pathlib import Path

from config.config import settings
from inverter.service import InverterService


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChargingService:
    def __init__(self, dry_run: bool):
        self.inverter_service = InverterService()
        self.dry_run = dry_run
        self.charging_state_file = Path(settings.charging_state_file)
        self.charging_state = self.fetch_charging_state()

    def fetch_charging_state(self) -> dict[str, any]:
        if self.charging_state_file.exists():
            with open(self.charging_state_file, "r") as file:
                state = json.load(file)
                logger.info(f"Fetched charging state: {state}")
                return state

        return {"charging_amps": 0, "charging_stopped": False}

    def save_charging_state(self):
        with open(self.charging_state_file, "w") as file:
            json.dump(self.charging_state, file, indent=4)

        logger.info(f"Saved charging state: {self.charging_state}")

    def smart_charge(self):
        inverter_data = self.inverter_service.fetch_data()

        max_available_power_kw = min(
            inverter_data.production_kw + settings.battery_max_power_kw, settings.inverter_max_power_kw
        )

        available_power_kw = max_available_power_kw - inverter_data.consumption_kw

        logger.info(f"Available power: {available_power_kw} kW")

        new_amps = self.calculate_new_amps(available_power_kw)

        if new_amps <= 0:
            self.stop_charging()
        else:
            if self.charging_state.get("charging_stopped", False):
                self.start_charging()

            self.set_charging_amps(new_amps)

        self.save_charging_state()

    @staticmethod
    def calculate_new_amps(available_power_kw: float) -> int:
        voltage = settings.voltage
        max_amps = int((available_power_kw * 1000) / 3 / voltage)
        logger.info(f"Calculated new amps: {max_amps}A for available power: {available_power_kw} kW")
        return max(0, max_amps)  # Ensure amps are non-negative

    def run_command(self, command: str):
        if self.dry_run:
            logger.info(f"Would run command: {command}")
            return

        logger.info(f"Running command: {command}")
        command = f"tesla-control -ble -vin {settings.tesla_vin} -key-name  {settings.tesla_key_name} {command}"
        subprocess.run(command, shell=True, check=True)

    def set_charging_amps(self, amps: int):
        if self.charging_state.get("charging_amps", 0) == amps:
            return

        logger.info(f"Setting charging amps to: {amps}")
        self.charging_state = {"charging_amps": amps, "charging_stopped": False}
        command = f"charging-set-amps {amps}"
        self.run_command(command)

    def stop_charging(self):
        if self.charging_state.get("charging_stopped", False):
            return

        logger.info("Stopping charging")
        self.charging_state["charging_stopped"] = True
        command = "charging-stop"
        self.run_command(command)

    def start_charging(self):
        if not self.charging_state.get("charging_stopped", False):
            return

        logger.info("Starting charging")
        self.charging_state["charging_stopped"] = False
        command = "charging-start"
        self.run_command(command)
