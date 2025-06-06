import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from options_trading.pricing import OptionContract
from options_trading.greeks import calculate_greeks


def test_delta_call():
    contract = OptionContract(
        underlying_price=100,
        strike=100,
        time_to_expiry=1,
        risk_free_rate=0.05,
        volatility=0.2,
        option_type="call",
    )
    greeks = calculate_greeks(contract)
    assert math.isclose(greeks.delta, 0.636, rel_tol=1e-2)

