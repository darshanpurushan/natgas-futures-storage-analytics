import pandas as pd
import pytest
from natgas_analytics.metrics import max_drawdown, performance_metrics

def test_max_drawdown():
    assert max_drawdown(pd.Series([0.10, -0.20, 0.05])) < 0

def test_metrics():
    m = performance_metrics(pd.Series([0.01, -0.005, 0.02, 0.01] * 20))
    assert "sharpe_ratio" in m
    assert m["total_return"] > 0

@pytest.mark.parametrize("returns, expected", [
    ([-.2], -.2),
    ([-.2, .1], -.2),
    ([-.2, -.1], -.28),
    ([.1, -.2], -.2),
    ([0., .1], 0.),
])
def test_drawdown_includes_starting_capital(returns, expected):
    series = pd.Series(returns)
    assert max_drawdown(series) == pytest.approx(expected)
    assert performance_metrics(series)["max_drawdown"] == pytest.approx(expected)
