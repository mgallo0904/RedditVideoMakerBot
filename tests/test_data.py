import pandas as pd
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from options_trading.data import fetch_price_history


def test_fetch_price_history():
    dummy = pd.DataFrame({"Close": [1.0, 2.0]}, index=pd.date_range("2020-01-01", periods=2))
    with patch("yfinance.download", return_value=dummy) as mock_dl:
        prices = fetch_price_history("AAPL", "2020-01-01", "2020-01-02")
        mock_dl.assert_called_once()
        assert isinstance(prices, pd.Series)
        assert prices.iloc[0] == 1.0

