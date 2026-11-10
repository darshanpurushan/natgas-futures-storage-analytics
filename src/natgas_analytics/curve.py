from __future__ import annotations

import numpy as np
import pandas as pd


def curve_matrix(curve):
    return curve.pivot_table(
        index="date", columns="contract", values="price", aggfunc="last"
    ).sort_index(axis=1)


def add_curve_metrics(curve):
    matrix = curve_matrix(curve)
    if matrix.shape[1] < 2:
        raise ValueError("At least two contract maturities are required.")

    periods = pd.PeriodIndex(matrix.columns.astype(str), freq="M")
    order = np.argsort(periods.asi8)
    matrix = matrix.iloc[:, order]

    # Listed maturities change over time. Select the nearest two observed
    # contracts per date instead of fixing the first pair in the history.
    available_order = np.argsort(matrix.isna().to_numpy(), axis=1, kind="stable")
    nearest = np.take_along_axis(matrix.to_numpy(), available_order[:, :2], axis=1)
    front = pd.Series(nearest[:, 0], index=matrix.index)
    second = pd.Series(nearest[:, 1], index=matrix.index)

    out = pd.DataFrame(index=matrix.index)
    out["front_price"] = front
    out["second_price"] = second
    out["calendar_spread"] = second - front
    out["calendar_spread_pct"] = (second - front) / front
    out["curve_state"] = np.where(
        out["calendar_spread"] > 0,
        "contango",
        np.where(out["calendar_spread"] < 0, "backwardation", "flat"),
    )
    out["curve_state"] = out["curve_state"].where(front.notna() & second.notna())
    out["annualized_roll_yield_proxy"] = (second / front) ** 12 - 1
    return out


def term_structure_snapshot(curve, date=None):
    matrix = curve_matrix(curve)
    date = matrix.index.max() if date is None else pd.Timestamp(date)
    row = matrix.loc[date].rename("price").reset_index()
    row.columns = ["contract", "price"]
    return row
