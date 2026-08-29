from dataclasses import dataclass

from src.market_data import Candle
from src.strategy import Signal, generate_signal


@dataclass(frozen=True)
class BacktestResult:
    starting_balance: float
    ending_balance: float
    trades: int

    @property
    def profit_loss(self) -> float:
        return self.ending_balance - self.starting_balance


def run_backtest(
    candles: list[Candle],
    starting_balance: float,
) -> BacktestResult:
    """Run a simple long/short-free strategy simulation."""

    if starting_balance <= 0:
        raise ValueError("Starting balance must be greater than zero.")

    if len(candles) < 2:
        raise ValueError("At least two candles are required.")

    balance = starting_balance
    trades = 0

    for previous, current in zip(candles, candles[1:]):
        signal = generate_signal(
            fast_price=current.close,
            slow_price=previous.close,
        )

        if signal == Signal.BUY:
            balance += current.close - previous.close
            trades += 1

        elif signal == Signal.SELL:
            balance += previous.close - current.close
            trades += 1

    return BacktestResult(
        starting_balance=starting_balance,
        ending_balance=balance,
        trades=trades,
    )
