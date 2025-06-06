"""Automated options strategy recommendation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .pricing import OptionContract, black_scholes_price
from .greeks import calculate_greeks


@dataclass
class Strategy:
    name: str
    description: str
    contracts: List[OptionContract]


def recommend_strategy(contract: OptionContract) -> Strategy:
    """Suggest a simple strategy based on volatility and Greeks."""
    greeks = calculate_greeks(contract)
    price = black_scholes_price(contract)
    if greeks.vega > price * 0.1:
        return Strategy(
            name="Straddle",
            description="Buy call and put at the same strike to play volatility",
            contracts=[contract, OptionContract(**{**contract.__dict__, "option_type": "put"})],
        )
    return Strategy(name="Covered Call", description="Hold underlying and sell call", contracts=[contract])

