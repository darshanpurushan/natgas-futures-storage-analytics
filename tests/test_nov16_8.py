import pandas as pd
import pytest
from natgas_analytics.backtest import build_signals
@pytest.mark.parametrize("dates", [[pd.Timestamp("2020-01-01")]*2,[pd.Timestamp("2020-01-01"),pd.NaT]])
def test_ambiguous_signal_dates(dates):
    with pytest.raises(ValueError,match="dates"):
        build_signals(pd.DataFrame({"date":dates,"calendar_spread":[1,2],"storage_surprise_z":[0,0]}))
