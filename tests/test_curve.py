import pandas as pd
from natgas_analytics.curve import add_curve_metrics

def test_calendar_spread():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-01", "2025-01-01"]),
        "contract": ["2025-02", "2025-03"],
        "price": [3.0, 3.3],
    })
    out = add_curve_metrics(df)
    assert abs(out.iloc[0]["calendar_spread"] - 0.3) < 1e-9
    assert out.iloc[0]["curve_state"] == "contango"
