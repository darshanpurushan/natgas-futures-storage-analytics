from unittest.mock import patch
import pandas as pd
import pytest
from natgas_analytics.backtest import run_backtest

def run(spreads,positions,cost=0.):
    frame=pd.DataFrame({'calendar_spread':spreads,'position':positions})
    with patch('natgas_analytics.backtest.build_signals',return_value=frame):
        return run_backtest(frame,transaction_cost=cost)[0]

def test_a_rising_negative_spread_profits_a_long_position():
    assert run([-2.,-1.],[0.,1.])['strategy_return'].iloc[1] == pytest.approx(.5)

def test_exit_cost_is_not_erased_when_previous_spread_is_zero():
    out=run([-1.,0.,1.],[0.,1.,0.],cost=.1)
    assert out['strategy_return'].iloc[2] == pytest.approx(-.1)
    assert out['equity'].iloc[2] == pytest.approx(1.9*.9)

def test_active_exposure_with_zero_base_is_rejected():
    with pytest.raises(ValueError,match='undefined active'):
        run([-1.,0.,1.],[0.,0.,1.])
