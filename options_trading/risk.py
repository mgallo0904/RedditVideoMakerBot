"""Risk management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass
class Portfolio:
    positions: Sequence[float]


def value_at_risk(portfolio_returns: Sequence[float], confidence: float = 0.95) -> float:
    """Historical simulation VaR."""
    losses = -np.sort(-np.array(portfolio_returns))
    index = int((1 - confidence) * len(losses))
    return losses[index]


