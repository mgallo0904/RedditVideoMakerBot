import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from options_trading.pricing import OptionContract, black_scholes_price


def test_black_scholes_call():
    contract = OptionContract(
        underlying_price=100,
        strike=100,
        time_to_expiry=1,
        risk_free_rate=0.05,
        volatility=0.2,
        option_type="call",
    )
    price = black_scholes_price(contract)
    # Known analytic value for parameters above is around 10.45
    assert math.isclose(price, 10.45, rel_tol=1e-2)

