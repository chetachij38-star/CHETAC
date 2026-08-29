import pytest

from src.backtest import run_backtest
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


def test_backtest_returns_result():
    candles = [
        make_candle(1, 100),
        make_candle(2, 101),
        make_candle(3, 102),
    ]

    result = run_backtest(candles, 1000)

    assert result.starting_balance == 1000
    assert result.ending_balance > 1000
    assert result.trades == 2


def test_rejects_insufficient_candles():
    candles = [make_candle(1, 100)]

    with pytest.raises(ValueError):
        run_backtest(candles, 1000)


def test_rejects_invalid_starting_balance():
    candles = [
        make_candle(1, 100),
        make_candle(2, 101),
    ]

    with pytest.raises(ValueError):
        run_backtest(candles, 0)
