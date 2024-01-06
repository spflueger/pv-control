import math
from datetime import datetime

import pandas as pd
from pv_system import PVPanelGroup, PVSystem
from suncalc import get_position

from .weather import make_forecast


class PowerEstimator:
    def __init__(self, longitude: float, latitude: float, pv_system: PVSystem) -> None:
        self.__LONGITUDE = longitude
        self.__LATITUDE = latitude
        self.__SUN_ALTITUDE = get_position(datetime.now(), longitude, latitude)[
            "altitude"
        ]
        self.__pv_system = pv_system

    def __estimate_power(
        self,
        panel_group: PVPanelGroup,
        direct_normal_radiation_in_watt_per_m2: float,
        diffuse_radiation_in_watt_per_m2: float,
    ):
        return (
            panel_group.square_meter_per_panel
            * panel_group.panel_count
            * panel_group.panel_efficiency
            * (
                diffuse_radiation_in_watt_per_m2
                * math.cos(math.radians(panel_group.horizontal_panel_angle_degrees))
                + (
                    direct_normal_radiation_in_watt_per_m2
                    * math.cos(
                        math.radians(
                            panel_group.horizontal_panel_angle_degrees
                            - self.__SUN_ALTITUDE
                        )
                    )  # the direct normal radiation is defined by the axis of the sun, so if the panel normal axis coninsides
                    if panel_group.directly_radiated
                    else 0.0
                )
            )
        )

    def make_power_forecast(self):
        weather_forecast = make_forecast(
            latitude=self.__LATITUDE, longitude=self.__LONGITUDE, days=1
        )

        forecast_data = {pg.name: [] for pg in self.__pv_system.panel_groups}
        forecast_data["date"] = []

        for index, row in weather_forecast.iterrows():
            timestamp = row["date"]
            diffuse_watt_per_square_meter = row["diffuse_radiation"]
            direct_normal_watt_per_square_meter = row["direct_normal_irradiance"]
            forecast_data["date"].append(timestamp)
            for panel_group in self.__pv_system.panel_groups:
                forecast_data[panel_group.name].append(
                    sum(
                        self.__estimate_power(
                            panel_area,
                            direct_normal_watt_per_square_meter,
                            diffuse_watt_per_square_meter,
                        )
                        for panel_area in panel_group.panel_areas
                    )
                )

        df = pd.DataFrame(data=forecast_data)
        df["total"] = df.loc[:, [x.name for x in self.__pv_system.panel_groups]].sum(
            axis=1
        )
        return df
