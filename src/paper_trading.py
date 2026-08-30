from dataclasses import dataclass

from src.execution import calculate_net_trade_result
from src.market_data import Candle
from src.risk import (
    calculate_risk_position_size,
    risk_gate,
)
from src.strategy import Signal, generate_signal


@dataclass(frozen=True)
class PaperTradingResult:
    starting_balance: float
    ending_balance: float
    trades: int


def run_paper_trading(
    candles: list[Candle],
    starting_balance: float,
    risk_percent: float,
    max_exposure_percent: float,
    max_daily_loss_percent: float,
    fee_rate: float,
    slippage_per_unit: float,
) -> PaperTradingResult:
    """Run a deterministic paper-trading simulation without real orders."""

    if starting_balance <= 0:
        raise ValueError("Starting balance must be greater than zero.")

    if len(candles) < 2:
        raise ValueError("At least two candles are required.")

    balance = starting_balance
    trades = 0
    starting_day_balance = starting_balance

    for previous, current in zip(candles, candles[1:]):
        signal = generate_signal(
            fast_price=current.close,
            slow_price=previous.close,
        )

        if signal == Signal.HOLD:
            continue

        direction = "long" if signal == Signal.BUY else "short"

        stop_loss_percent = 5.0

        stop_loss_price = (
            previous.close * (1 - stop_loss_percent / 100)
            if direction == "long"
            else previous.close * (1 + stop_loss_percent / 100)
        )

        position_size = calculate_risk_position_size(
            account_balance=balance,
            risk_percent=risk_percent,
            entry_price=previous.close,
            stop_loss_price=stop_loss_price,
        )

        position_value = position_size * previous.close

        if not risk_gate(
            account_balance=balance,
            position_value=position_value,
            max_exposure_percent=max_exposure_percent,
            starting_day_balance=starting_day_balance,
            current_balance=balance,
            max_daily_loss_percent=max_daily_loss_percent,
        ):
            continue

        if direction == "long":
            trade_result = calculate_net_trade_result(
                entry_price=previous.close,
                exit_price=current.close,
                position_size=position_size,
                fee_rate=fee_rate,
                slippage_per_unit=slippage_per_unit,
            )
        else:
            trade_result = calculate_net_trade_result(
                entry_price=current.close,
                exit_price=previous.close,
                position_size=position_size,
                fee_rate=fee_rate,
                slippage_per_unit=slippage_per_unit,
            )

        balance += trade_result
        trades += 1

    return PaperTradingResult(
        starting_balance=starting_balance,
        ending_balance=balance,
        trades=trades,
    )
