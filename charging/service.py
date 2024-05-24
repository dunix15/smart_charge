import json
import logging
import subprocess
import time
from pathlib import Path

from charging.schema import ChargingState
from config.config import settings
from inverter.service import InverterService


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)


class ChargingService:
    def __init__(self, use_battery: bool = True, dry_run: bool = False):
        self.use_battery = use_battery
        self.dry_run = dry_run
        self.inverter_service = InverterService()
        self.state_file = Path(settings.charging_state_file)
        self.state: ChargingState = self.fetch_state()
        log.info(f"Initial charging state: {self.state}")

    def fetch_state(self) -> ChargingState:
        if self.state_file.exists():
            with open(self.state_file, "r") as file:
                state = json.load(file)
                return ChargingState(**state)

        return ChargingState(
            inverter_data=None, amps=self.calculate_new_amps(settings.inverter_max_power_kw), is_active=True
        )

    def save_charging_state(self):
        with open(self.state_file, "w") as file:
            json.dump(self.state.dict(), file, indent=4)

        log.info(f"Saved charging state: {self.state}")

    def smart_charge(self):
        inverter_data = self.inverter_service.fetch_data()
        if inverter_data == self.state.inverter_data:
            return

        self.state.inverter_data = inverter_data
        log.info(f"Fetched inverter data: {inverter_data}")

        available_max_power_kw = inverter_data.production_kw
        if self.use_battery and inverter_data.battery_soc > settings.battery_min_soc:
            available_max_power_kw += settings.battery_max_power_kw

        available_max_power_kw = min(available_max_power_kw, settings.inverter_max_power_kw)

        net_consumption_kw = max(inverter_data.consumption_kw - self.state.amps * settings.voltage * 3 / 1000, 0)

        available_power_kw = available_max_power_kw - net_consumption_kw

        log.info(f"Available power: {available_power_kw} kW")

        new_amps = self.calculate_new_amps(available_power_kw)

        if new_amps < 3:
            self.stop_charging()
        else:
            if not self.state.is_active:
                self.start_charging()

            self.set_charging_amps(new_amps)

        self.save_charging_state()

    def run_in_background(self):
        while True:
            self.smart_charge()
            time.sleep(60)

    @staticmethod
    def calculate_new_amps(available_power_kw: float) -> int:
        voltage = settings.voltage
        max_amps = int((available_power_kw * 1000) / 3 / voltage)
        log.info(f"Calculated new amps: {max_amps}A for available power: {available_power_kw} kW")
        return max(0, max_amps)  # Ensure amps are non-negative

    def run_command(self, command: str):
        if self.dry_run:
            log.info(f"Would run command: {command}")
            return

        log.info(f"Running command: {command}")
        command = f"tesla-control -ble -vin {settings.tesla_vin} -key-name  {settings.tesla_key_name} {command}"
        subprocess.run(command, shell=True, check=True)

    def set_charging_amps(self, amps: int):
        if self.state.amps == amps:
            return

        log.info(f"Setting charging amps to: {amps}")
        self.state.amps = amps
        self.state.is_active = True
        command = f"charging-set-amps {amps}"
        self.run_command(command)

    def stop_charging(self):
        if not self.state.is_active:
            return

        log.info("Stopping charging")
        self.state.amps = 0
        self.state.is_active = False
        command = "charging-stop"
        self.run_command(command)

    def start_charging(self):
        if self.state.is_active:
            return

        log.info("Starting charging")
        self.state.is_active = True
        command = "charging-start"
        self.run_command(command)
