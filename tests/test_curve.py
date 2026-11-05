import pandas as pd
import pytest
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

def test_front_pair_rolls_with_each_dates_available_contracts():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-02"] * 2 + ["2025-02-03"] * 2),
        "contract": ["2025-02", "2025-03", "2025-03", "2025-04"],
        "price": [3.0, 3.3, 3.4, 3.2],
    })
    out = add_curve_metrics(df.sample(frac=1, random_state=7))
    assert out["front_price"].tolist() == [3.0, 3.4]
    assert out["second_price"].tolist() == [3.3, 3.2]
    assert out["calendar_spread"].tolist() == pytest.approx([.3, -.2])
    assert out["curve_state"].tolist() == ["contango", "backwardation"]


def test_incomplete_front_pair_is_not_classified_as_flat():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-02"] * 2 + ["2025-02-03"]),
        "contract": ["2025-02", "2025-03", "2025-03"],
        "price": [3.0, 3.3, 3.4],
    })
    out = add_curve_metrics(df)
    assert out.iloc[-1]["front_price"] == 3.4
    assert pd.isna(out.iloc[-1]["second_price"])
    assert pd.isna(out.iloc[-1]["curve_state"])
