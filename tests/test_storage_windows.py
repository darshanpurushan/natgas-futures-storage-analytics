import numpy as np
import pandas as pd
import pytest

from natgas_analytics.storage import storage_features


@pytest.mark.parametrize("lookback", [2, 4, 12])
def test_short_storage_windows_use_available_window_length(lookback):
    storage = pd.DataFrame({"date": pd.date_range("2025-01-01", periods=40),
                            "storage_bcf": 1000. + np.arange(40) ** 3})
    out = storage_features(storage, lookback=lookback)
    expected = storage["storage_bcf"].diff().rolling(lookback, min_periods=min(12, lookback)).mean()
    pd.testing.assert_series_equal(out["seasonal_change_mean"], expected, check_names=False)
    assert out["storage_surprise_z"].notna().any()


@pytest.mark.parametrize("lookback", [0, 1, True, 2.5])
def test_invalid_storage_windows_have_clear_errors(lookback):
    with pytest.raises(ValueError, match="lookback must be an integer"):
        storage_features(pd.DataFrame({"date": [], "storage_bcf": []}), lookback=lookback)
