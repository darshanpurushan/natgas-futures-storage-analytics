import pandas as pd
import pytest

from natgas_analytics.curve import add_curve_metrics


@pytest.mark.parametrize("second,months", [("2025-03", 1), ("2025-04", 2), ("2025-08", 6)])
def test_roll_proxy_uses_actual_month_gap(second, months):
    curve = pd.DataFrame({"date": pd.to_datetime(["2025-01-02"] * 2),
                          "contract": ["2025-02", second], "price": [3., 3.3]})
    out = add_curve_metrics(curve)
    assert out.iloc[0]["annualized_roll_yield_proxy"] == pytest.approx(1.1 ** (12 / months) - 1)


def test_maturity_gap_follows_selected_pair_on_each_date():
    curve = pd.DataFrame({"date": pd.to_datetime(["2025-01-02"] * 2 + ["2025-02-03"] * 2),
                          "contract": ["2025-02", "2025-04", "2025-03", "2025-04"],
                          "price": [3., 3.3, 3., 3.3]})
    out = add_curve_metrics(curve)
    assert out["annualized_roll_yield_proxy"].tolist() == pytest.approx([1.1 ** 6 - 1, 1.1 ** 12 - 1])
