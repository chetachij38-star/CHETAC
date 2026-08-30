from src.execution import calculate_net_trade_result
from src.market_data import Candle
from src.risk import calculate_risk_position_size, risk_gate
from src.strategy import Signal, generate_signal
from src.trade import Trade, TradeResult


def test_end_to_end_trade_flow():
    previous = Candle(
        timestamp=1,
        open=100,
        high=101,
        low=99,
        close=100,
        volume=1000,
    )

    current = Candle(
        timestamp=2,
        open=100,
        high=106,
        low=99,
        close=105,
        volume=1200,
    )

    signal = generate_signal(
        fast_price=current.close,
        slow_price=previous.close,
    )

    assert signal == Signal.BUY

    entry_price = previous.close
    stop_loss_price = 95

    position_size = calculate_risk_position_size(
        account_balance=1000,
        risk_percent=1,
        entry_price=entry_price,
        stop_loss_price=stop_loss_price,
    )

    position_value = position_size * entry_price

    allowed = risk_gate(
        account_balance=1000,
        position_value=position_value,
        max_exposure_percent=30,
        starting_day_balance=1000,
        current_balance=1000,
        max_daily_loss_percent=5,
    )

    assert allowed is True

    trade = Trade(
        direction="long",
        entry_price=entry_price,
        exit_price=current.close,
        position_size=position_size,
    )

    net_result = calculate_net_trade_result(
        entry_price=trade.entry_price,
        exit_price=trade.exit_price,
        position_size=trade.position_size,
        fee_rate=0.001,
        slippage_per_unit=0.01,
    )

    result = TradeResult(
        direction=trade.direction,
        entry_price=trade.entry_price,
        exit_price=trade.exit_price,
        position_size=trade.position_size,
        net_result=net_result,
    )

    assert result.net_result > 0
