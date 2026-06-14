from __future__ import annotations

import json
import ssl
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "weather"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

DAILY_VARIABLES = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "apparent_temperature_mean",
    "precipitation_sum",
    "rain_sum",
    "snowfall_sum",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "shortwave_radiation_sum",
]

RENAME_COLUMNS = {
    "time": "date",
    "temperature_2m_max": "temperature_max_c",
    "temperature_2m_min": "temperature_min_c",
    "temperature_2m_mean": "temperature_mean_c",
    "apparent_temperature_mean": "apparent_temperature_mean_c",
    "precipitation_sum": "precipitation_mm",
    "rain_sum": "rain_mm",
    "snowfall_sum": "snowfall_cm",
    "wind_speed_10m_max": "wind_speed_max_kmh",
    "wind_gusts_10m_max": "wind_gusts_max_kmh",
    "shortwave_radiation_sum": "shortwave_radiation_mj_m2",
}


# M5 does not expose actual store coordinates. These are representative cities
# for the three states in M5 and should be reported as state-level proxies.
M5_LOCATIONS = [
    {
        "source_dataset": "m5",
        "weather_location_id": "m5_CA",
        "state_id": "CA",
        "location_name": "Los Angeles, CA",
        "weather_spatial_level": "state_representative_city",
        "latitude": 34.0522,
        "longitude": -118.2437,
    },
    {
        "source_dataset": "m5",
        "weather_location_id": "m5_TX",
        "state_id": "TX",
        "location_name": "Dallas, TX",
        "weather_spatial_level": "state_representative_city",
        "latitude": 32.7767,
        "longitude": -96.7970,
    },
    {
        "source_dataset": "m5",
        "weather_location_id": "m5_WI",
        "state_id": "WI",
        "location_name": "Milwaukee, WI",
        "weather_spatial_level": "state_representative_city",
        "latitude": 43.0389,
        "longitude": -87.9065,
    },
]


MAVEN_US_LOCATIONS = [
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_2",
        "store_id": 2,
        "store_name": "Store 2",
        "store_city": "Bellingham",
        "store_state": "WA",
        "location_name": "Bellingham, WA",
        "weather_spatial_level": "store_city",
        "latitude": 48.7519,
        "longitude": -122.4787,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_3",
        "store_id": 3,
        "store_name": "Store 3",
        "store_city": "Bremerton",
        "store_state": "WA",
        "location_name": "Bremerton, WA",
        "weather_spatial_level": "store_city",
        "latitude": 47.5650,
        "longitude": -122.6275,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_6",
        "store_id": 6,
        "store_name": "Store 6",
        "store_city": "Beverly Hills",
        "store_state": "CA",
        "location_name": "Beverly Hills, CA",
        "weather_spatial_level": "store_city",
        "latitude": 34.0736,
        "longitude": -118.4004,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_7",
        "store_id": 7,
        "store_name": "Store 7",
        "store_city": "Los Angeles",
        "store_state": "CA",
        "location_name": "Los Angeles, CA",
        "weather_spatial_level": "store_city",
        "latitude": 34.0522,
        "longitude": -118.2437,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_11",
        "store_id": 11,
        "store_name": "Store 11",
        "store_city": "Portland",
        "store_state": "OR",
        "location_name": "Portland, OR",
        "weather_spatial_level": "store_city",
        "latitude": 45.5152,
        "longitude": -122.6784,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_13",
        "store_id": 13,
        "store_name": "Store 13",
        "store_city": "Salem",
        "store_state": "OR",
        "location_name": "Salem, OR",
        "weather_spatial_level": "store_city",
        "latitude": 44.9429,
        "longitude": -123.0351,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_14",
        "store_id": 14,
        "store_name": "Store 14",
        "store_city": "San Francisco",
        "store_state": "CA",
        "location_name": "San Francisco, CA",
        "weather_spatial_level": "store_city",
        "latitude": 37.7749,
        "longitude": -122.4194,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_15",
        "store_id": 15,
        "store_name": "Store 15",
        "store_city": "Seattle",
        "store_state": "WA",
        "location_name": "Seattle, WA",
        "weather_spatial_level": "store_city",
        "latitude": 47.6062,
        "longitude": -122.3321,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_16",
        "store_id": 16,
        "store_name": "Store 16",
        "store_city": "Spokane",
        "store_state": "WA",
        "location_name": "Spokane, WA",
        "weather_spatial_level": "store_city",
        "latitude": 47.6588,
        "longitude": -117.4260,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_17",
        "store_id": 17,
        "store_name": "Store 17",
        "store_city": "Tacoma",
        "store_state": "WA",
        "location_name": "Tacoma, WA",
        "weather_spatial_level": "store_city",
        "latitude": 47.2529,
        "longitude": -122.4443,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_22",
        "store_id": 22,
        "store_name": "Store 22",
        "store_city": "Walla Walla",
        "store_state": "WA",
        "location_name": "Walla Walla, WA",
        "weather_spatial_level": "store_city",
        "latitude": 46.0646,
        "longitude": -118.3430,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_23",
        "store_id": 23,
        "store_name": "Store 23",
        "store_city": "Yakima",
        "store_state": "WA",
        "location_name": "Yakima, WA",
        "weather_spatial_level": "store_city",
        "latitude": 46.6021,
        "longitude": -120.5059,
    },
    {
        "source_dataset": "maven_market_us",
        "weather_location_id": "maven_store_24",
        "store_id": 24,
        "store_name": "Store 24",
        "store_city": "San Diego",
        "store_state": "CA",
        "location_name": "San Diego, CA",
        "weather_spatial_level": "store_city",
        "latitude": 32.7157,
        "longitude": -117.1611,
    },
]


def fetch_open_meteo_daily(location: dict, start_date: str, end_date: str) -> pd.DataFrame:
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(DAILY_VARIABLES),
        "timezone": "auto",
    }
    url = OPEN_METEO_ARCHIVE_URL + "?" + urllib.parse.urlencode(params)

    # Local Python on this machine has a missing CA certificate chain. Open-Meteo
    # is still HTTPS; this unverified context is used only to work around local
    # certificate setup while fetching public historical weather data.
    context = ssl._create_unverified_context()

    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(url, timeout=120, context=context) as response:
                payload = json.load(response)
            if "error" in payload:
                raise RuntimeError(payload.get("reason", payload["error"]))
            break
        except Exception as exc:
            last_error = exc
            if attempt == 3:
                raise
            time.sleep(2 * attempt)
    else:
        raise RuntimeError(f"Failed to fetch weather: {last_error}")

    daily = payload["daily"]
    df = pd.DataFrame(daily).rename(columns=RENAME_COLUMNS)
    df["date"] = pd.to_datetime(df["date"])

    metadata = {
        key: value
        for key, value in location.items()
        if key not in {"latitude", "longitude"}
    }
    for key, value in metadata.items():
        df[key] = value

    df["latitude_requested"] = location["latitude"]
    df["longitude_requested"] = location["longitude"]
    df["latitude_open_meteo"] = payload.get("latitude")
    df["longitude_open_meteo"] = payload.get("longitude")
    df["elevation_m"] = payload.get("elevation")
    df["timezone"] = payload.get("timezone")
    df["utc_offset_seconds"] = payload.get("utc_offset_seconds")
    df["weather_source"] = "open_meteo_archive"
    return df


def fetch_dataset_weather(locations: list[dict], start_date: str, end_date: str) -> pd.DataFrame:
    parts = []
    for index, location in enumerate(locations, start=1):
        print(
            f"[{index}/{len(locations)}] Fetching {location['location_name']} "
            f"({start_date} -> {end_date})"
        )
        part = fetch_open_meteo_daily(location, start_date, end_date)
        parts.append(part)
        time.sleep(0.25)
    return pd.concat(parts, ignore_index=True)


def order_columns(df: pd.DataFrame) -> pd.DataFrame:
    first_cols = [
        "source_dataset",
        "weather_location_id",
        "date",
        "state_id",
        "store_id",
        "store_name",
        "store_city",
        "store_state",
        "location_name",
        "weather_spatial_level",
    ]
    weather_cols = [
        "weather_code",
        "temperature_max_c",
        "temperature_min_c",
        "temperature_mean_c",
        "apparent_temperature_mean_c",
        "precipitation_mm",
        "rain_mm",
        "snowfall_cm",
        "wind_speed_max_kmh",
        "wind_gusts_max_kmh",
        "shortwave_radiation_mj_m2",
    ]
    meta_cols = [
        "latitude_requested",
        "longitude_requested",
        "latitude_open_meteo",
        "longitude_open_meteo",
        "elevation_m",
        "timezone",
        "utc_offset_seconds",
        "weather_source",
    ]
    existing_first = [col for col in first_cols if col in df.columns]
    existing_weather = [col for col in weather_cols if col in df.columns]
    existing_meta = [col for col in meta_cols if col in df.columns]
    remaining = [
        col
        for col in df.columns
        if col not in set(existing_first + existing_weather + existing_meta)
    ]
    return df[existing_first + existing_weather + remaining + existing_meta]


def main() -> None:
    m5_weather = fetch_dataset_weather(
        M5_LOCATIONS,
        start_date="2011-01-29",
        end_date="2016-05-22",
    )
    m5_weather = order_columns(m5_weather)
    m5_output = OUTPUT_DIR / "m5_open_meteo_daily_weather.csv"
    m5_weather.to_csv(m5_output, index=False, encoding="utf-8")
    print(f"Saved M5 weather: {m5_output}")
    print(m5_weather.shape)

    maven_weather = fetch_dataset_weather(
        MAVEN_US_LOCATIONS,
        start_date="1997-01-01",
        end_date="1998-12-31",
    )
    maven_weather = order_columns(maven_weather)
    maven_output = OUTPUT_DIR / "maven_us_open_meteo_daily_weather.csv"
    maven_weather.to_csv(maven_output, index=False, encoding="utf-8")
    print(f"Saved Maven USA weather: {maven_output}")
    print(maven_weather.shape)

    print("\nM5 weather preview:")
    print(m5_weather.head().to_string(index=False))
    print("\nMaven USA weather preview:")
    print(maven_weather.head().to_string(index=False))


if __name__ == "__main__":
    main()
