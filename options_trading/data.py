"""Market data utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yfinance as yf

import pandas as pd


def load_price_history(csv_path: Path, symbol: Optional[str] = None) -> pd.Series:
    """Load historical prices from a CSV file."""
    df = pd.read_csv(csv_path, parse_dates=["date"])
    if symbol:
        df = df[df["symbol"] == symbol]
    return df.set_index("date")["close"]


def fetch_price_history(symbol: str, start: str, end: str, interval: str = "1d") -> pd.Series:
    """Fetch historical closing prices from Yahoo Finance.

    Parameters
    ----------
    symbol: str
        The ticker symbol to download, e.g. ``"AAPL"``.
    start: str
        Start date as ``"YYYY-MM-DD"``.
    end: str
        End date as ``"YYYY-MM-DD"``.
    interval: str, optional
        Data interval supported by Yahoo Finance. Defaults to ``"1d"``.

    Returns
    -------
    pandas.Series
        Series of closing prices indexed by date.
    """
    data = yf.download(symbol, start=start, end=end, interval=interval, progress=False)
    if "Close" not in data:
        raise ValueError(f"Failed to fetch data for {symbol}")
    return data["Close"]

