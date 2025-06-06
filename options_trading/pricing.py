"""Option pricing models."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.stats import norm


@dataclass
class OptionContract:
    underlying_price: float
    strike: float
    time_to_expiry: float  # in years
    risk_free_rate: float
    volatility: float
    option_type: str  # 'call' or 'put'


def _d1(contract: OptionContract) -> float:
    return (
        math.log(contract.underlying_price / contract.strike)
        + (contract.risk_free_rate + 0.5 * contract.volatility ** 2)
        * contract.time_to_expiry
    ) / (contract.volatility * math.sqrt(contract.time_to_expiry))


def _d2(contract: OptionContract) -> float:
    return _d1(contract) - contract.volatility * math.sqrt(contract.time_to_expiry)


def black_scholes_price(contract: OptionContract) -> float:
    """Price an option using the Black-Scholes formula."""
    d1 = _d1(contract)
    d2 = _d2(contract)
    if contract.option_type == "call":
        price = (
            contract.underlying_price * norm.cdf(d1)
            - contract.strike * math.exp(-contract.risk_free_rate * contract.time_to_expiry) * norm.cdf(d2)
        )
    else:
        price = (
            contract.strike * math.exp(-contract.risk_free_rate * contract.time_to_expiry) * norm.cdf(-d2)
            - contract.underlying_price * norm.cdf(-d1)
        )
    return price


def binomial_price(contract: OptionContract, steps: int = 100) -> float:
    """Price an option using a Cox-Ross-Rubinstein binomial tree."""
    dt = contract.time_to_expiry / steps
    u = math.exp(contract.volatility * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(contract.risk_free_rate * dt) - d) / (u - d)
    disc = math.exp(-contract.risk_free_rate * dt)

    prices = [contract.underlying_price * (u ** j) * (d ** (steps - j)) for j in range(steps + 1)]
    if contract.option_type == "call":
        values = [max(0, price - contract.strike) for price in prices]
    else:
        values = [max(0, contract.strike - price) for price in prices]

    for _ in range(steps):
        values = [disc * (p * values[j + 1] + (1 - p) * values[j]) for j in range(len(values) - 1)]
    return values[0]


def monte_carlo_price(contract: OptionContract, simulations: int = 10000) -> float:
    """Price an option using Monte Carlo simulation."""
    dt = contract.time_to_expiry
    drift = (contract.risk_free_rate - 0.5 * contract.volatility ** 2) * dt
    diffusion = contract.volatility * math.sqrt(dt)
    z = np.random.standard_normal(simulations)
    price = contract.underlying_price * np.exp(drift + diffusion * z)
    if contract.option_type == "call":
        payoff = np.maximum(price - contract.strike, 0)
    else:
        payoff = np.maximum(contract.strike - price, 0)
    return math.exp(-contract.risk_free_rate * dt) * np.mean(payoff)

