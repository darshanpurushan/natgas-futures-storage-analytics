import numpy as np
import pandas as pd
import pytest

from natgas_analytics.metrics import max_drawdown, performance_metrics


@pytest.mark.parametrize('calculate', [max_drawdown, performance_metrics])
@pytest.mark.parametrize('values', [[-2., -2.], [np.inf], [-np.inf]])
def test_invalid_wealth_factors_cannot_be_reported_as_performance(calculate, values):
    with pytest.raises(ValueError, match='finite.*-100%'):
        calculate(pd.Series(values))


def test_exact_total_loss_remains_valid():
    metrics = performance_metrics(pd.Series([.1, -1., .2]))
    assert metrics['total_return'] == -1.
    assert metrics['annualized_return'] == -1.
    assert metrics['max_drawdown'] == -1.


def test_missing_observations_keep_existing_neutral_handling():
    returns = pd.Series([np.nan, -.2, .1])
    metrics = performance_metrics(returns)
    assert metrics['total_return'] == pytest.approx(-.12)
    assert metrics['max_drawdown'] == pytest.approx(-.2)
    assert max_drawdown(returns) == pytest.approx(-.2)
