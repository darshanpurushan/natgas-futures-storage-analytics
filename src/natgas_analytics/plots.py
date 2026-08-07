from __future__ import annotations

import matplotlib.pyplot as plt


def save_curve_plot(metrics, path):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(metrics.index, metrics["front_price"], label="Front")
    ax.plot(metrics.index, metrics["second_price"], label="Second")
    ax.set_title("Henry Hub Front Two Contracts")
    ax.set_ylabel("Price")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_spread_plot(metrics, path):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(metrics.index, metrics["calendar_spread"])
    ax.axhline(0, linewidth=1)
    ax.set_title("Front Calendar Spread: Second - Front")
    ax.set_ylabel("Price difference")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_storage_plot(storage, path):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(storage["date"], storage["storage_bcf"])
    ax.set_title("Working Natural Gas in Storage")
    ax.set_ylabel("Bcf")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_backtest_plot(backtest, path):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(backtest["date"], backtest["equity"])
    ax.set_title("Normalized Calendar-Spread Strategy Equity")
    ax.set_ylabel("Growth of $1")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
