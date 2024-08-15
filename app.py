import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from charging.schema import ChargingState
from charging.service import ChargingService
from inverter.schema import InverterData

log = logging.getLogger(__name__)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Serve static files from the 'static' directory
app.mount("/app", StaticFiles(directory="static", html=True), name="static")

service = ChargingService()
# service.run_in_background()

state_file = Path("state.json")


@app.get("/state", response_model=ChargingState)
def get_state():
    return service.fetch_state()


@app.get("/inverter-data", response_model=InverterData)
def get_inverter_data():
    state = service.fetch_state()
    return state.inverter_data


class UpdateStateModel(BaseModel):
    is_active: bool
    use_battery: bool


@app.post("/state", response_model=ChargingState)
def update_state(data: UpdateStateModel):
    for field in ("is_active", "use_battery"):
        setattr(service.state, field, getattr(data, field))

    if not service.state.is_active:
        service.stop_charging()

    service.save_charging_state()

    return service.state
