from dataclasses import dataclass

from src.trade import TradeResult


@dataclass(frozen=True)
class PaperPerformanceReport:
    starting_balance: float
    ending_balance: float
    total_return_percent: float
    trades: int
    win_rate: float
    profit_factor: float
    max_drawdown: float
    equity_curve: list[float]


def build_paper_performance(
    starting_balance: float,
    trade_results: list[TradeResult],
) -> PaperPerformanceReport:
    """Build measurable performance statistics from paper trades."""

    if starting_balance <= 0:
        raise ValueError("Starting balance must be greater than zero.")

    equity_curve = [starting_balance]
    balance = starting_balance

    for trade in trade_results:
        balance += trade.net_result
        equity_curve.append(balance)

    ending_balance = balance
    trades = len(trade_results)

    total_return_percent = (
        (ending_balance - starting_balance) / starting_balance
    ) * 100

    winning_trades = [
        trade.net_result
        for trade in trade_results
        if trade.net_result > 0
    ]

    losing_trades = [
        trade.net_result
        for trade in trade_results
        if trade.net_result < 0
    ]

    win_rate = (
        len(winning_trades) / trades * 100
        if trades
        else 0.0
    )

    gross_profit = sum(winning_trades)
    gross_loss = abs(sum(losing_trades))

    if gross_loss:
        profit_factor = gross_profit / gross_loss
    else:
        profit_factor = float("inf") if gross_profit else 0.0

    peak = equity_curve[0]
    max_drawdown = 0.0

    for equity in equity_curve:
        peak = max(peak, equity)
        if peak > 0:
            drawdown = ((peak - equity) / peak) * 100
            max_drawdown = max(max_drawdown, drawdown)

    return PaperPerformanceReport(
        starting_balance=starting_balance,
        ending_balance=ending_balance,
        total_return_percent=total_return_percent,
        trades=trades,
        win_rate=win_rate,
        profit_factor=profit_factor,
        max_drawdown=max_drawdown,
        equity_curve=equity_curve,
    )
