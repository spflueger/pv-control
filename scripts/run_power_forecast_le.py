from datetime import datetime

import pandas as pd
from suncalc import get_times

from forecast.energy import predict_daily_energy
from forecast.power import PowerEstimator
from pv_system import PVPanelArea, PVPanelGroup, PVSystem

# config

# Leinfelden
LATITUDE = 48.7007
LONGITUDE = 9.1383

SUNRISE_TIME = get_times(datetime.now(), LONGITUDE, LATITUDE)["sunrise"]
SUNSET_TIME = get_times(datetime.now(), LONGITUDE, LATITUDE)["sunset"]

PANEL_AREA = 1.953882
PANEL_EFFICIENCY = 0.2
SOUTH_PANELS = 25
SOUTH_GAUBE_PANELS = 10
NORTH_GAUBE_PANELS = 7
GARAGE_PANELS = 12

south_wo_gaube = PVPanelArea(
    SOUTH_PANELS - SOUTH_GAUBE_PANELS, PANEL_AREA, PANEL_EFFICIENCY, 45
)
south_gaube = PVPanelArea(SOUTH_GAUBE_PANELS, PANEL_AREA, PANEL_EFFICIENCY, 25)

south_panel_group = PVPanelGroup("Süddach", [south_wo_gaube, south_gaube])

north_gaube = PVPanelArea(
    NORTH_GAUBE_PANELS, PANEL_AREA, PANEL_EFFICIENCY, 25, directly_radiated=False
)
garage = PVPanelArea(
    GARAGE_PANELS, PANEL_AREA, PANEL_EFFICIENCY, 25, directly_radiated=False
)

north_panel_group = PVPanelGroup("Nordgaube+Garage", [north_gaube, garage])

# run

print("sunrise", SUNRISE_TIME)
print("sunset", SUNSET_TIME)

power_estimator = PowerEstimator(
    LONGITUDE,
    LATITUDE,
    pv_system=PVSystem("PV Anlage", [south_panel_group, north_panel_group]),
)

power_forecast = power_estimator.make_power_forecast()
energy_predictions = predict_daily_energy(power_forecast)

print("predicted daily pv energy", energy_predictions.daily_energy_forecast)
print(
    "predicted daily remaining pv energy",
    energy_predictions.daily_remaining_energy_forecast,
)
with pd.option_context(
    "display.max_rows", None, "display.max_columns", None
):  # more options can be specified also
    print(power_forecast)

# so we make the weather forecast and get the predictions for watts per hour for the rest of the day

# then based on this we decide how
