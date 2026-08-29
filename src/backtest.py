from src.execution import calculate_net_trade_result
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


def calculate_position_size(
    balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float,
) -> float:
    """Calculate units based on a fixed percentage of account risk."""

    if balance <= 0:
        raise ValueError("Balance must be greater than zero.")

    if risk_percent <= 0:
        raise ValueError("Risk percent must be greater than zero.")

    if entry_price <= 0 or stop_loss_price <= 0:
        raise ValueError("Prices must be greater than zero.")

    if entry_price == stop_loss_price:
        raise ValueError("Entry and stop-loss prices cannot be equal.")

    risk_amount = balance * (risk_percent / 100)
    stop_distance = abs(entry_price - stop_loss_price)

    return risk_amount / stop_distance


def calculate_trade_cost(
    position_size: float,
    entry_price: float,
    exit_price: float,
    fee_rate: float,
    slippage_rate: float,
) -> float:
    """Calculate estimated trading costs from fees and slippage."""

    if position_size <= 0:
        raise ValueError("Position size must be greater than zero.")

    if entry_price <= 0 or exit_price <= 0:
        raise ValueError("Prices must be greater than zero.")

    if fee_rate < 0:
        raise ValueError("Fee rate cannot be negative.")

    if slippage_rate < 0:
        raise ValueError("Slippage rate cannot be negative.")

    traded_value = position_size * (entry_price + exit_price)

    fee_cost = traded_value * fee_rate
    slippage_cost = traded_value * slippage_rate

    return fee_cost + slippage_cost


def calculate_return_percent(
    starting_balance: float,
    ending_balance: float,
) -> float:
    """Calculate account return as a percentage."""

    if starting_balance <= 0:
        raise ValueError("Starting balance must be greater than zero.")

    return ((ending_balance - starting_balance) / starting_balance) * 100


def calculate_win_rate(trade_results: list[float]) -> float:
    """Calculate the percentage of trades with positive results."""

    if not trade_results:
        return 0.0

    winning_trades = sum(1 for result in trade_results if result > 0)

    return (winning_trades / len(trade_results)) * 100


def build_equity_curve(
    starting_balance: float,
    trade_results: list[float],
) -> list[float]:
    """Build account equity after each completed trade."""

    if starting_balance <= 0:
        raise ValueError("Starting balance must be greater than zero.")

    equity_curve = [starting_balance]
    balance = starting_balance

    for result in trade_results:
        balance += result
        equity_curve.append(balance)

    return equity_curve


@dataclass(frozen=True)
class BacktestReport:
    starting_balance: float
    ending_balance: float
    total_return_percent: float
    trades: int
    win_rate: float
    profit_factor: float
    max_drawdown: float
    equity_curve: list[float]


def build_backtest_report(
    starting_balance: float,
    trade_results: list[float],
) -> BacktestReport:
    """Build a consolidated performance report from trade results."""

    if starting_balance <= 0:
        raise ValueError("Starting balance must be greater than zero.")

    equity_curve = build_equity_curve(starting_balance, trade_results)
    ending_balance = equity_curve[-1]
    trades = len(trade_results)

    total_return_percent = (
        (ending_balance - starting_balance) / starting_balance
    ) * 100

    winning_trades = [result for result in trade_results if result > 0]
    losing_trades = [result for result in trade_results if result < 0]

    win_rate = (
        len(winning_trades) / trades * 100
        if trades
        else 0.0
    )

    gross_profit = sum(winning_trades)
    gross_loss = abs(sum(losing_trades))

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss
        else float("inf") if gross_profit else 0.0
    )

    peak = equity_curve[0]
    max_drawdown = 0.0

    for equity in equity_curve:
        peak = max(peak, equity)
        drawdown = peak - equity
        max_drawdown = max(max_drawdown, drawdown)

    return BacktestReport(
        starting_balance=starting_balance,
        ending_balance=ending_balance,
        total_return_percent=total_return_percent,
        trades=trades,
        win_rate=win_rate,
        profit_factor=profit_factor,
        max_drawdown=max_drawdown,
        equity_curve=equity_curve,
    )


def run_cost_aware_backtest(
    candles: list[Candle],
    starting_balance: float,
    position_size: float,
    fee_rate: float,
    slippage_per_unit: float,
) -> BacktestResult:
    """Run the strategy simulation using the execution cost model."""

    if starting_balance <= 0:
        raise ValueError("Starting balance must be greater than zero.")

    if len(candles) < 2:
        raise ValueError("At least two candles are required.")

    if position_size <= 0:
        raise ValueError("Position size must be greater than zero.")

    balance = starting_balance
    trades = 0

    for previous, current in zip(candles, candles[1:]):
        signal = generate_signal(
            fast_price=current.close,
            slow_price=previous.close,
        )

        if signal == Signal.BUY:
            trade_result = calculate_net_trade_result(
                entry_price=previous.close,
                exit_price=current.close,
                position_size=position_size,
                fee_rate=fee_rate,
                slippage_per_unit=slippage_per_unit,
            )
            balance += trade_result
            trades += 1

        elif signal == Signal.SELL:
            trade_result = calculate_net_trade_result(
                entry_price=current.close,
                exit_price=previous.close,
                position_size=position_size,
                fee_rate=fee_rate,
                slippage_per_unit=slippage_per_unit,
            )
            balance += trade_result
            trades += 1

    return BacktestResult(
        starting_balance=starting_balance,
        ending_balance=balance,
        trades=trades,
    )
