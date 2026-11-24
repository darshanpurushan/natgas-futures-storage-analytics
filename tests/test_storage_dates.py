import pandas as pd
import pytest

from natgas_analytics.storage import storage_features


@pytest.mark.parametrize("dates", [
    pd.to_datetime(["2025-01-01", "2025-01-01", "2025-01-08"]),
    pd.to_datetime(["2025-01-01", None, "2025-01-08"]),
])
def test_ambiguous_storage_dates_are_rejected(dates):
    frame = pd.DataFrame({"date": dates, "storage_bcf": [100., 120., 110.]})
    with pytest.raises(ValueError, match="Storage dates must be present and unique"):
        storage_features(frame, lookback=2)


def test_unsorted_unique_observations_keep_chronological_changes():
    frame = pd.DataFrame({"date": pd.to_datetime(["2025-01-15", "2025-01-01", "2025-01-08"]),
                          "storage_bcf": [115., 100., 120.]})
    out = storage_features(frame, lookback=2)
    assert out.storage_change_bcf.iloc[1:].tolist() == [20., -5.]
    assert out.date.is_monotonic_increasing
