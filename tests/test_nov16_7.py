import pandas as pd
import pytest
from natgas_analytics.backtest import run_backtest
@pytest.mark.parametrize("cost", [-1,float("nan"),float("inf")])
def test_invalid_cost(cost):
    df=pd.DataFrame({"date":pd.date_range("2020-01-01",periods=20),"calendar_spread":[1]*20,"storage_surprise_z":[0]*20})
    with pytest.raises(ValueError,match="transaction_cost"):
        run_backtest(df,transaction_cost=cost)
