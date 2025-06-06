"""AI-powered options trading utilities."""

from .pricing import OptionContract, black_scholes_price, binomial_price, monte_carlo_price
from .greeks import calculate_greeks, Greeks
from .strategies import recommend_strategy, Strategy
from .ml_models import lstm_price_predictor, VolatilityForecaster
from .risk import value_at_risk, Portfolio
from .backtesting import backtest
from .data import load_price_history, fetch_price_history

__all__ = [
    "OptionContract",
    "black_scholes_price",
    "binomial_price",
    "monte_carlo_price",
    "calculate_greeks",
    "Greeks",
    "recommend_strategy",
    "Strategy",
    "lstm_price_predictor",
    "VolatilityForecaster",
    "value_at_risk",
    "Portfolio",
    "backtest",
    "load_price_history",
    "fetch_price_history",
]

