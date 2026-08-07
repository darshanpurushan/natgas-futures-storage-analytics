# Natural Gas Futures Curve & Storage Analytics

research project for Henry Hub futures-curve analytics, EIA storage, weather extensions, and a transparent calendar-spread backtest.


## Quick start

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
pytest
python -m natgas_analytics.pipeline --demo
```

The default demo is deterministic and needs no API keys.

## What is included

- Futures curve construction from long-format CSV data
- Contango / backwardation classification
- Front calendar spread
- Annualized roll-yield proxy
- EIA weekly storage download
- Storage-change surprise z-score
- NOAA daily temperature helper
- Rule-based calendar-spread strategy
- Lagged signals to avoid basic look-ahead bias
- Sharpe ratio, annualized return/volatility, max drawdown
- Research CSV outputs and charts
- Unit tests
- Jupyter walkthrough

## Project layout

```text
natgas-futures-storage-analytics/
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── .env.example
├── data/raw/.gitkeep
├── data/processed/.gitkeep
├── reports/.gitkeep
├── notebooks/01_research_walkthrough.ipynb
├── src/natgas_analytics/
│   ├── __init__.py
│   ├── config.py
│   ├── data.py
│   ├── curve.py
│   ├── storage.py
│   ├── weather.py
│   ├── backtest.py
│   ├── metrics.py
│   ├── plots.py
│   └── pipeline.py
└── tests/
    ├── test_curve.py
    ├── test_metrics.py
    └── test_backtest.py
```

## Live data

Set an EIA API key:

```bash
export EIA_API_KEY="your_key"
```

Then:

```bash
python -m natgas_analytics.pipeline --live
```

For a real historical futures curve, provide a CSV:

```csv
date,contract,price
2025-01-02,2025-02,3.20
2025-01-02,2025-03,3.31
2025-01-02,2025-04,3.42
```

Run:

```bash
python -m natgas_analytics.pipeline --curve-csv path/to/curve.csv
```

### Important data caveat

A complete historical futures curve needs contract-level historical prices. A continuous `NG=F` series is not enough. The live-mode convenience code therefore creates a clearly marked synthetic second maturity; replace it with actual contract data before using the research results.

## Strategy

The educational strategy combines two z-scores:

1. Storage surprise relative to a rolling historical mean.
2. Front calendar-spread deviation from its rolling mean.

It goes long the spread when both are unusually low and short when both are unusually high. The signal is shifted by one observation before returns are applied.

The backtest uses normalized spread returns rather than dollar futures P&L. A production-quality model should add contract multipliers, tick values, margin, slippage, liquidity, expiration, roll rules, and transaction costs calibrated to the instrument.

## Suggested extensions

- EIA five-year storage normal
- HDD/CDD weather variables
- Analyst-consensus inventory surprise
- Regression of spread changes on storage shocks
- Contract expiration and roll logic
- Transaction-cost sensitivity
- Walk-forward / out-of-sample testing
- Streamlit dashboard
