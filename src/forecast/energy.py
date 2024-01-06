from datetime import datetime, timedelta
from typing import List

import pandas as pd
from attrs import define
from dateutil import tz


@define
class PVEnergyForecast:
    daily_remaining_energy_forecast: float
    daily_energy_forecast: float


def _integrate_power_over_time(
    t: List[datetime],
    p: List[float],
    t_start: datetime,
    t_end: datetime = None,
):
    if t_end is None:
        t_end = t[-1]

    total_energy = 0.0
    time_interval = (
        t[1] - t[0]
    ).total_seconds() / 3600  # Assuming equal time intervals

    # Generate an artificial time point before the first time point
    t_artificial = t[0] - timedelta(hours=time_interval)

    # Adjusted loop to include the artificial time point
    for i, power in enumerate(p):
        start_time = t_artificial if i == 0 else t[i - 1]
        end_time = t[i]

        # Adjusting start and end times if they fall within the interval
        adjusted_start = max(start_time, t_start)
        adjusted_end = min(end_time, t_end)

        if adjusted_end <= adjusted_start:
            continue

        # Calculation
        interval_hours = (adjusted_end - adjusted_start).total_seconds() / 3600
        total_energy += interval_hours * power

    return total_energy


def predict_daily_energy(power_forecast: pd.DataFrame) -> PVEnergyForecast:
    return PVEnergyForecast(
        daily_remaining_energy_forecast=_integrate_power_over_time(
            power_forecast["date"].to_numpy(),
            power_forecast["total"].to_numpy(),
            t_start=datetime.now(tz=tz.gettz("Europe/Berlin")),
        ),
        daily_energy_forecast=_integrate_power_over_time(
            power_forecast["date"].to_numpy(),
            power_forecast["total"].to_numpy(),
            t_start=datetime.now(tz=tz.gettz("Europe/Berlin")).replace(
                hour=0, minute=0, second=0
            ),
        ),
    )
