from __future__ import annotations

import requests
import pandas as pd

NOAA_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"


def download_noaa_daily(token, station, start, end):
    if not token or not station:
        raise ValueError("NOAA_TOKEN and NOAA_STATION are required.")

    r = requests.get(
        NOAA_URL,
        headers={"token": token},
        params={
            "datasetid": "GHCND",
            "stationid": station,
            "startdate": start,
            "enddate": end,
            "datatypeid": "TAVG",
            "units": "standard",
            "limit": 1000,
        },
        timeout=30,
    )
    r.raise_for_status()
    df = pd.DataFrame(r.json().get("results", []))
    if df.empty:
        return pd.DataFrame(columns=["date", "tavg_f"])

    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    df["tavg_f"] = pd.to_numeric(df["value"], errors="coerce")
    return df[["date", "tavg_f"]].dropna()


def weekly_temperature(weather):
    if weather.empty:
        return weather.copy()
    return (
        weather.set_index("date")["tavg_f"]
        .resample("W-THU")
        .mean()
        .rename("tavg_f")
        .reset_index()
    )
