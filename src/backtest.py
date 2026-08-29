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


def calculate_max_drawdown(equity_curve: list[float]) -> float:
    """Return maximum peak-to-trough decline as a percentage."""

    if not equity_curve:
        raise ValueError("Equity curve cannot be empty.")

    peak = equity_curve[0]
    max_drawdown = 0.0

    for equity in equity_curve:
        if equity > peak:
            peak = equity

        if peak > 0:
            drawdown = ((peak - equity) / peak) * 100
            max_drawdown = max(max_drawdown, drawdown)

    return max_drawdown


def calculate_profit_factor(
    profits: list[float],
    losses: list[float],
) -> float:
    """Return gross profits divided by absolute gross losses."""

    gross_profit = sum(value for value in profits if value > 0)
    gross_loss = abs(sum(value for value in losses if value < 0))

    if gross_loss == 0:
        return float("inf") if gross_profit > 0 else 0.0

    return gross_profit / gross_loss
