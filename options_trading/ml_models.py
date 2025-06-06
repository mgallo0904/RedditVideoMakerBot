"""Machine learning models for options trading."""

from __future__ import annotations

from torch import nn


def lstm_price_predictor(input_size: int, hidden_size: int = 50, num_layers: int = 2) -> nn.Module:
    """Return a simple LSTM network for price prediction."""

    class LSTMModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
            self.fc = nn.Linear(hidden_size, 1)

        def forward(self, x):
            out, _ = self.lstm(x)
            out = out[:, -1, :]
            return self.fc(out)

    return LSTMModel()


class VolatilityForecaster(nn.Module):
    """A simple neural network for volatility forecasting."""

    def __init__(self, input_size: int, hidden_size: int = 32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1),
        )

    def forward(self, x):
        return self.net(x)

