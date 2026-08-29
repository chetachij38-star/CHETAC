import pytest

from src.backtest import run_cost_aware_backtest
from src.market_data import Candle


def make_candle(timestamp: int, close: float) -> Candle:
    return Candle(
        timestamp=timestamp,
        open=close,
        high=close + 1,
        low=close - 1,
        close=close,
        volume=100,
    )


def test_cost_aware_backtest_applies_trading_costs():
    candles = [
        make_candle(1, 100),
        make_candle(2, 101),
        make_candle(3, 102),
    ]

    result = run_cost_aware_backtest(
        candles=candles,
        starting_balance=1000,
        position_size=1,
        fee_rate=0.001,
        slippage_per_unit=0.0,
    )

    assert result.starting_balance == 1000
    assert result.trades == 2
    assert result.ending_balance < 1002


def test_cost_aware_backtest_rejects_invalid_position_size():
    candles = [
        make_candle(1, 100),
        make_candle(2, 101),
    ]

    with pytest.raises(ValueError):
        run_cost_aware_backtest(
            candles=candles,
            starting_balance=1000,
            position_size=0,
            fee_rate=0.001,
            slippage_per_unit=0.0,
        )
