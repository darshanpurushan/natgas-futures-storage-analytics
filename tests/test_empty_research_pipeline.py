from unittest.mock import Mock

import pandas as pd
import pytest

from natgas_analytics import pipeline


def test_empty_research_does_not_overwrite_existing_reports(tmp_path, monkeypatch):
    reports = tmp_path / "reports"
    processed = tmp_path / "processed"
    reports.mkdir()
    existing = reports / "performance_metrics.txt"
    existing.write_text("previous valid report")
    monkeypatch.setattr(pipeline, "REPORTS", reports)
    monkeypatch.setattr(pipeline, "DATA_PROCESSED", processed)
    for name in ("save_curve_plot", "save_spread_plot", "save_storage_plot", "save_backtest_plot"):
        monkeypatch.setattr(pipeline, name, Mock())
    date = pd.Timestamp("2025-01-01")
    curve = pd.DataFrame({"date": [date, date], "contract": ["2025-02", "2025-03"], "price": [2., 3.]})
    storage = pd.DataFrame({"date": [date], "storage_bcf": [100.]})
    with pytest.raises(ValueError, match="No usable research observations"):
        pipeline.run(curve, storage)
    assert existing.read_text() == "previous valid report"
    assert not list(processed.glob("*.csv"))
    pipeline.save_backtest_plot.assert_not_called()


def test_usable_research_still_writes_reports(tmp_path, monkeypatch):
    from natgas_analytics.data import make_demo_curve
    from natgas_analytics.storage import make_demo_storage

    monkeypatch.setattr(pipeline, "REPORTS", tmp_path / "reports")
    monkeypatch.setattr(pipeline, "DATA_PROCESSED", tmp_path / "processed")
    for name in ("save_curve_plot", "save_spread_plot", "save_storage_plot", "save_backtest_plot"):
        monkeypatch.setattr(pipeline, name, Mock())
    pipeline.run(make_demo_curve(end="2019-12-31"), make_demo_storage(end="2019-12-31"))
    research = pd.read_csv(tmp_path / "processed" / "research_dataset.csv")
    assert not research.empty
    assert (tmp_path / "reports" / "performance_metrics.txt").exists()
    pipeline.save_backtest_plot.assert_called_once()
