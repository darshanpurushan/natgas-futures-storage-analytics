from __future__ import annotations

import requests
import pandas as pd
import time

NOAA_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"


def download_noaa_daily(token, station, start, end):
    if not token or not station:
        raise ValueError("NOAA_TOKEN and NOAA_STATION are required.")

    first, last = pd.Timestamp(start), pd.Timestamp(end)
    if pd.isna(first) or pd.isna(last) or first > last:
        raise ValueError("Invalid NOAA date range")
    first, last = first.normalize(), last.normalize()
    rows, calls = [], 0
    # NOAA limits daily data requests to a year and collection pages to
    # 1000 records. Keep requests below both limits, including leap years.
    cursor = first
    while cursor <= last:
        window_end = min(cursor + pd.Timedelta(days=364), last)
        offset = 1
        while True:
            if calls:
                time.sleep(.21)  # documented token limit: five requests/second
            calls += 1
            r = requests.get(NOAA_URL, headers={"token": token}, params={
                "datasetid": "GHCND", "stationid": station,
                "startdate": cursor.date().isoformat(),
                "enddate": window_end.date().isoformat(),
                "datatypeid": "TAVG", "units": "standard",
                "limit": 1000, "offset": offset,
            }, timeout=30)
            r.raise_for_status()
            payload = r.json()
            page = payload.get("results", [])
            count = int(payload.get("metadata", {}).get("resultset", {}).get("count", len(page)))
            if not page:
                if offset <= count:
                    raise RuntimeError("NOAA pagination ended before the advertised record count")
                break
            rows.extend(page)
            if offset + len(page) > count:
                break
            offset += len(page)
        cursor = window_end + pd.Timedelta(days=1)
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=["date", "tavg_f"])

    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    df["tavg_f"] = pd.to_numeric(df["value"], errors="coerce")
    return df[["date", "tavg_f"]].dropna().sort_values("date").reset_index(drop=True)


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
