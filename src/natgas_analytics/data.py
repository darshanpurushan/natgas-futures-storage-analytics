from __future__ import annotations

import numpy as np
import pandas as pd


def make_demo_curve(start="2018-01-01", end="2025-12-31", seed=7):
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start, end, freq="W-THU")
    rows = []

    for date in dates:
        base = 2.8 + 0.55 * np.cos(2 * np.pi * (date.month - 1) / 12)
        base += rng.normal(0, 0.12)
        for months_ahead in range(1, 13):
            contract = (date.to_period("M") + months_ahead).strftime("%Y-%m")
            term = 0.025 * months_ahead
            winter = 0.08 * np.cos(
                2 * np.pi * (pd.Period(contract, freq="M").month - 1) / 12
            )
            price = max(0.8, base + term + winter + rng.normal(0, 0.035))
            rows.append({"date": date, "contract": contract, "price": price})

    return pd.DataFrame(rows)


def load_curve_csv(path):
    df = pd.read_csv(path, parse_dates=["date"])
    required = {"date", "contract", "price"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Curve CSV is missing columns: {sorted(missing)}")
    df["contract"] = df["contract"].astype(str)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df.dropna(subset=["date", "contract", "price"]).sort_values(
        ["date", "contract"]
    )


def download_front_month_yahoo(start="2018-01-01", end="2026-01-01"):
    import yfinance as yf

    data = yf.download(
        "NG=F", start=start, end=end, auto_adjust=False, progress=False
    )
    if data.empty:
        raise RuntimeError("Yahoo Finance returned no data for NG=F.")

    close = data["Close"]
    if getattr(close, "ndim", 1) > 1:
        close = close.iloc[:, 0]

    return pd.DataFrame({"date": close.index, "price": close.values}).dropna()
