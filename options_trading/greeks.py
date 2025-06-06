"""Greeks calculation for option contracts."""

from __future__ import annotations

import math
from dataclasses import dataclass

from scipy.stats import norm

from .pricing import OptionContract, _d1, _d2


@dataclass
class Greeks:
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


def calculate_greeks(contract: OptionContract) -> Greeks:
    """Return the option Greeks using Black-Scholes sensitivities."""
    d1 = _d1(contract)
    d2 = _d2(contract)
    sign = 1 if contract.option_type == "call" else -1
    delta = sign * norm.cdf(sign * d1)
    gamma = norm.pdf(d1) / (contract.underlying_price * contract.volatility * math.sqrt(contract.time_to_expiry))
    theta = (
        -(
            contract.underlying_price
            * norm.pdf(d1)
            * contract.volatility
            / (2 * math.sqrt(contract.time_to_expiry))
        )
        - sign
        * contract.risk_free_rate
        * contract.strike
        * math.exp(-contract.risk_free_rate * contract.time_to_expiry)
        * norm.cdf(sign * d2)
    )
    vega = contract.underlying_price * norm.pdf(d1) * math.sqrt(contract.time_to_expiry)
    rho = sign * contract.strike * contract.time_to_expiry * math.exp(-contract.risk_free_rate * contract.time_to_expiry) * norm.cdf(sign * d2)
    return Greeks(delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)

