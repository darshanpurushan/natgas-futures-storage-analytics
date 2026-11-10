from __future__ import annotations

import requests
import pandas as pd

EIA_URL = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/"


def download_eia_storage(api_key, start="2010-01-01", end=None):
    if not api_key:
        raise ValueError("EIA_API_KEY is required for live EIA downloads.")

    params = {
        "api_key": api_key,
        "frequency": "weekly",
        "data[0]": "value",
        "facets[process][]": "S1",
        "facets[duoarea][]": "NUS",
        "start": start,
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "offset": 0,
        "length": 5000,
    }
    if end:
        params["end"] = end

    r = requests.get(EIA_URL, params=params, timeout=30)
    r.raise_for_status()
    rows = r.json().get("response", {}).get("data", [])
    if not rows:
        raise RuntimeError("EIA returned no storage observations.")

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["period"])
    df["storage_bcf"] = pd.to_numeric(df["value"], errors="coerce")
    return df[["date", "storage_bcf"]].dropna().sort_values("date")


def make_demo_storage(start="2018-01-01", end="2025-12-31", seed=7):
    rng = __import__("numpy").random.default_rng(seed)
    dates = pd.date_range(start, end, freq="W-THU")
    t = __import__("numpy").arange(len(dates))
    seasonal = 900 * __import__("numpy").cos(
        2 * __import__("numpy").pi * (dates.dayofyear - 45) / 365.25
    )
    storage = 3200 + seasonal + 0.35 * t + rng.normal(0, 70, len(dates)).cumsum()
    return pd.DataFrame({"date": dates, "storage_bcf": storage})


def storage_features(storage, lookback=52):
    if isinstance(lookback, bool) or not isinstance(lookback, int) or lookback < 2:
        raise ValueError("lookback must be an integer of at least 2")
    min_periods = min(12, lookback)
    df = storage.copy().sort_values("date")
    df["storage_change_bcf"] = df["storage_bcf"].diff()
    df["seasonal_change_mean"] = df["storage_change_bcf"].rolling(
        lookback, min_periods=min_periods
    ).mean()
    df["storage_surprise_bcf"] = (
        df["storage_change_bcf"] - df["seasonal_change_mean"]
    )
    std = df["storage_surprise_bcf"].rolling(
        lookback, min_periods=min_periods
    ).std()
    df["storage_surprise_z"] = df["storage_surprise_bcf"] / std.replace(0, pd.NA)
    return df
