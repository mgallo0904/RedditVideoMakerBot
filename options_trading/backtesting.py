"""Simple backtesting engine."""

from __future__ import annotations

from typing import Callable

import pandas as pd

from .pricing import OptionContract


def backtest(prices: pd.Series, strategy_func: Callable[[float], OptionContract]) -> pd.Series:
    """Run a naive backtest over historical prices."""
    pnl = []
    for price in prices:
        contract = strategy_func(price)
        pnl.append(price - contract.strike)
    return pd.Series(pnl, index=prices.index)

