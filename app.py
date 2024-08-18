import logging
import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from contextlib import asynccontextmanager

from charging.schema import ChargingState
from charging.service import ChargingService
from inverter.schema import InverterData

log = logging.getLogger(__name__)


app = FastAPI()
# Serve static files from the 'static' directory
app.mount("/app", StaticFiles(directory="static", html=True), name="static")

service = ChargingService()

async def smart_charge_task():
    while True:
        service.smart_charge()
        await asyncio.sleep(20)  # Wait for 20 seconds before the next call


# Lifespan context manager to handle startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    task = asyncio.create_task(smart_charge_task())
    yield
    # Shutdown event
    task.cancel()
    await task


# Assign the lifespan context manager to the app
app.router.lifespan_context = lifespan


@app.get("/state", response_model=ChargingState)
def get_state():
    return service.state


@app.get("/inverter-data", response_model=InverterData)
def get_inverter_data():
    return service.inverter_service.fetch_data()


class UpdateStateModel(BaseModel):
    is_active: bool | None = None
    use_battery: bool | None = None
    inverter_max_power_kw: float | None = None
    battery_max_power_kw: float | None = None
    battery_min_soc: float | None = None
    voltage: float | None = None


@app.post("/state", response_model=ChargingState)
def update_state(data: UpdateStateModel):
    if service.state.is_active and not data.is_active:
        service.stop_charging()

    if not service.state.is_active and data.is_active:
        service.adjust_charging()

    for field, val in data:
        if val is not None:
            setattr(service.state, field, val)

    service.save_charging_state()

    return service.state
