from __future__ import annotations

import argparse
import pandas as pd

from .config import DATA_PROCESSED, REPORTS, EIA_API_KEY
from .data import make_demo_curve, load_curve_csv, download_front_month_yahoo
from .storage import make_demo_storage, download_eia_storage, storage_features
from .curve import add_curve_metrics
from .backtest import run_backtest
from .plots import save_curve_plot, save_spread_plot, save_storage_plot, save_backtest_plot


def run(curve, storage):
    REPORTS.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    curve_metrics = add_curve_metrics(curve).reset_index(names="date")
    storage_df = storage_features(storage)

    research = pd.merge_asof(
        curve_metrics.sort_values("date"),
        storage_df.sort_values("date"),
        on="date",
        direction="backward",
    ).dropna(subset=["storage_surprise_z", "calendar_spread"])

    backtest, metrics = run_backtest(research)

    curve_metrics.to_csv(DATA_PROCESSED / "curve_metrics.csv", index=False)
    storage_df.to_csv(DATA_PROCESSED / "storage_features.csv", index=False)
    research.to_csv(DATA_PROCESSED / "research_dataset.csv", index=False)
    backtest.to_csv(DATA_PROCESSED / "backtest_results.csv", index=False)

    save_curve_plot(curve_metrics.set_index("date"), REPORTS / "curve.png")
    save_spread_plot(curve_metrics.set_index("date"), REPORTS / "calendar_spread.png")
    save_storage_plot(storage_df, REPORTS / "storage.png")
    save_backtest_plot(backtest, REPORTS / "backtest_equity.png")

    with open(REPORTS / "performance_metrics.txt", "w", encoding="utf-8") as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value:.6f}\n")

    print("\nBacktest metrics")
    print("----------------")
    for key, value in metrics.items():
        print(f"{key:24s} {value: .4f}")
    print(f"\nReports: {REPORTS}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true")
    p.add_argument("--live", action="store_true")
    p.add_argument("--curve-csv")
    args = p.parse_args()

    if args.curve_csv:
        curve = load_curve_csv(args.curve_csv)
        storage = download_eia_storage(EIA_API_KEY) if EIA_API_KEY else make_demo_storage()
    elif args.live:
        front = download_front_month_yahoo()
        curve = front.assign(
            contract=front["date"].dt.to_period("M").astype(str)
        )
        # Convenience only: replace with real contract-level data for research.
        second = curve.copy()
        second["contract"] = (
            pd.to_datetime(second["date"]).dt.to_period("M") + 1
        ).astype(str)
        second["price"] *= 1.03
        curve = pd.concat([curve, second], ignore_index=True)
        storage = download_eia_storage(EIA_API_KEY) if EIA_API_KEY else make_demo_storage()
    else:
        curve, storage = make_demo_curve(), make_demo_storage()

    run(curve, storage)


if __name__ == "__main__":
    main()
