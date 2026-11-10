import pandas as pd
import pytest

from natgas_analytics.data import load_curve_csv
from natgas_analytics.curve import add_curve_metrics


def test_nonfinite_prices_are_dropped(tmp_path):
    path = tmp_path / "curve.csv"
    path.write_text("date,contract,price\n2025-01-02,2025-01,inf\n"
                    "2025-01-02,2025-02,3.0\n2025-01-02,2025-03,3.3\n"
                    "2025-01-02,2025-04,-inf\n")
    curve = load_curve_csv(path)
    assert curve["price"].tolist() == [3.0, 3.3]


def test_missing_contracts_are_dropped_before_string_conversion(tmp_path):
    path = tmp_path / "curve.csv"
    path.write_text("date,contract,price\n2025-01-02,,3.1\n"
                    "2025-01-02,2025-02,3.0\n2025-01-02,2025-03,3.3\n")
    curve = load_curve_csv(path)
    assert curve["contract"].tolist() == ["2025-02", "2025-03"]
    assert add_curve_metrics(curve).iloc[0]["calendar_spread"] == pytest.approx(.3)


@pytest.mark.parametrize("columns", ["contract,price\n2025-02,3.0\n",
                                      "date,price\n2025-01-02,3.0\n"])
def test_missing_columns_produce_schema_error(tmp_path, columns):
    path = tmp_path / "curve.csv"
    path.write_text(columns)
    with pytest.raises(ValueError, match="Curve CSV is missing columns"):
        load_curve_csv(path)
