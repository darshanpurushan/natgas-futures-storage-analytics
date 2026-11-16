import pandas as pd
import pytest
from natgas_analytics.metrics import performance_metrics
@pytest.mark.parametrize("frequency", [0,-1,float("nan"),float("inf")])
def test_invalid_frequency(frequency):
    with pytest.raises(ValueError,match="periods_per_year"):
        performance_metrics(pd.Series([.01,-.02]),periods_per_year=frequency)
