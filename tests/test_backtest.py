import pandas as pd
from natgas_analytics.backtest import build_signals

def test_signal_is_lagged():
    dates = pd.date_range("2025-01-01", periods=15, freq="W")
    df = pd.DataFrame({
        "date": dates,
        "calendar_spread": [-1.0] * 15,
        "storage_surprise_z": [-2.0] * 15,
    })
    out = build_signals(df)
    assert out.iloc[0]["position"] == 0
