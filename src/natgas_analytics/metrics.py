from __future__ import annotations

import numpy as np
import pandas as pd


def max_drawdown(returns):
    wealth = (1 + returns.fillna(0)).cumprod()
    return float((wealth / wealth.cummax() - 1).min())


def performance_metrics(returns, periods_per_year=52):
    r = returns.dropna()
    if r.empty:
        return {
            "total_return": 0.0,
            "annualized_return": 0.0,
            "annualized_volatility": 0.0,
            "sharpe_ratio": np.nan,
            "max_drawdown": 0.0,
        }

    wealth = (1 + r).cumprod()
    years = len(r) / periods_per_year
    total = wealth.iloc[-1] - 1
    annualized = wealth.iloc[-1] ** (1 / max(years, 1 / periods_per_year)) - 1
    vol = r.std(ddof=1) * np.sqrt(periods_per_year)
    sharpe = (
        r.mean() / r.std(ddof=1) * np.sqrt(periods_per_year)
        if r.std(ddof=1)
        else np.nan
    )

    return {
        "total_return": float(total),
        "annualized_return": float(annualized),
        "annualized_volatility": float(vol),
        "sharpe_ratio": float(sharpe),
        "max_drawdown": max_drawdown(r),
    }
