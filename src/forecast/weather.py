import openmeteo_requests
import pandas as pd
import requests_cache
from dateutil import tz
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"

from_zone = tz.gettz("GMT")
to_zone = tz.gettz("Europe/Berlin")


def make_forecast(latitude: float, longitude: float, days: int) -> pd.DataFrame:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "minutely_15": [
            "sunshine_duration",
            "is_day",
            "shortwave_radiation",
            "direct_radiation",
            "diffuse_radiation",
            "direct_normal_irradiance",
            "terrestrial_radiation",
        ],
        "hourly": [
            "weather_code",
            "cloud_cover",
            "cloud_cover_low",
            "cloud_cover_mid",
            "cloud_cover_high",
        ],
        "timezone": "Europe/Berlin",
        "forecast_days": days,
    }

    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process minutely_15 data. The order of variables needs to be the same as requested.
    minutely_15 = response.Minutely15()
    minutely_15_sunshine_duration = minutely_15.Variables(0).ValuesAsNumpy()
    minutely_15_is_day = minutely_15.Variables(1).ValuesAsNumpy()
    minutely_15_shortwave_radiation = minutely_15.Variables(2).ValuesAsNumpy()
    minutely_15_direct_radiation = minutely_15.Variables(3).ValuesAsNumpy()
    minutely_15_diffuse_radiation = minutely_15.Variables(4).ValuesAsNumpy()
    minutely_15_direct_normal_irradiance = minutely_15.Variables(5).ValuesAsNumpy()
    minutely_15_terrestrial_radiation = minutely_15.Variables(6).ValuesAsNumpy()

    minutely_15_data = {
        "date": pd.date_range(
            start=pd.to_datetime(minutely_15.Time(), unit="s")
            .replace(tzinfo=from_zone)
            .astimezone(to_zone),
            end=pd.to_datetime(minutely_15.TimeEnd(), unit="s")
            .replace(tzinfo=from_zone)
            .astimezone(to_zone),
            freq=pd.Timedelta(seconds=minutely_15.Interval()),
            inclusive="left",
        )
    }
    minutely_15_data["sunshine_duration"] = minutely_15_sunshine_duration
    minutely_15_data["is_day"] = minutely_15_is_day
    minutely_15_data["shortwave_radiation"] = minutely_15_shortwave_radiation
    minutely_15_data["direct_radiation"] = minutely_15_direct_radiation
    minutely_15_data["diffuse_radiation"] = minutely_15_diffuse_radiation
    minutely_15_data["direct_normal_irradiance"] = minutely_15_direct_normal_irradiance
    minutely_15_data["terrestrial_radiation"] = minutely_15_terrestrial_radiation

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_weather_code = hourly.Variables(0).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(1).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(2).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(3).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(4).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s")
            .replace(tzinfo=from_zone)
            .astimezone(to_zone),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s")
            .replace(tzinfo=from_zone)
            .astimezone(to_zone),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high

    dataframe = pd.DataFrame(data=minutely_15_data)
    dataframe = dataframe.merge(
        pd.DataFrame(data=hourly_data),
        left_on="date",
        right_on="date",
        how="left",
    )

    return dataframe
