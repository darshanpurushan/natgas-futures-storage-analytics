import pandas as pd
from natgas_analytics.metrics import max_drawdown, performance_metrics

def test_max_drawdown():
    assert max_drawdown(pd.Series([0.10, -0.20, 0.05])) < 0

def test_metrics():
    m = performance_metrics(pd.Series([0.01, -0.005, 0.02, 0.01] * 20))
    assert "sharpe_ratio" in m
    assert m["total_return"] > 0
