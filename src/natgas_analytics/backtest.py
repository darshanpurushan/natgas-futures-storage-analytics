from __future__ import annotations

import numpy as np

from .metrics import performance_metrics


def build_signals(df, storage_z_threshold=1.0, spread_z_threshold=1.0):
    x = df.copy().sort_values("date")
    mean = x["calendar_spread"].rolling(52, min_periods=12).mean()
    std = x["calendar_spread"].rolling(52, min_periods=12).std()
    x["spread_z"] = (x["calendar_spread"] - mean) / std.replace(0, np.nan)

    long_signal = (
        (x["storage_surprise_z"] < -storage_z_threshold)
        & (x["spread_z"] < -spread_z_threshold)
    )
    short_signal = (
        (x["storage_surprise_z"] > storage_z_threshold)
        & (x["spread_z"] > spread_z_threshold)
    )

    x["signal"] = np.select([long_signal, short_signal], [1.0, -1.0], default=0.0)
    x["position"] = x["signal"].shift(1).fillna(0.0)
    return x


def run_backtest(df, transaction_cost=0.0005):
    x = build_signals(df)
    # Normalize by spread magnitude: a long spread benefits from a rising
    # value even when the starting spread is negative. A zero denominator
    # cannot define an active normalized return.
    x["spread_return"] = x["calendar_spread"].diff() / x["calendar_spread"].shift(1).abs()
    active = x["position"] != 0
    if (active & ~np.isfinite(x["spread_return"])).any():
        raise ValueError("Cannot value undefined active spread returns")
    x["turnover"] = x["position"].diff().abs().fillna(x["position"].abs())
    x["strategy_return"] = (
        (x["position"] * x["spread_return"]).where(active, 0.)
        - transaction_cost * x["turnover"]
    )
    x["equity"] = (1 + x["strategy_return"].fillna(0)).cumprod()
    return x, performance_metrics(x["strategy_return"])
