import pytest

from src.market_data import Candle
from src.strategy import Signal, generate_signal, generate_candle_signal


def test_generates_buy_signal():
    assert generate_signal(101, 100) == Signal.BUY


def test_generates_sell_signal():
    assert generate_signal(99, 100) == Signal.SELL


def test_generates_hold_signal():
    assert generate_signal(100.05, 100) == Signal.HOLD


def test_rejects_invalid_prices():
    with pytest.raises(ValueError):
        generate_signal(0, 100)


def test_rejects_negative_threshold():
    with pytest.raises(ValueError):
        generate_signal(101, 100, -0.1)



def test_generates_buy_signal_from_bullish_candle():
    candle = Candle(
        timestamp=1,
        open=100,
        high=103,
        low=99,
        close=102,
        volume=100,
    )

    assert generate_candle_signal(candle) == Signal.BUY


def test_generates_sell_signal_from_bearish_candle():
    candle = Candle(
        timestamp=2,
        open=100,
        high=101,
        low=97,
        close=98,
        volume=100,
    )

    assert generate_candle_signal(candle) == Signal.SELL


def test_generates_hold_signal_from_small_candle():
    candle = Candle(
        timestamp=3,
        open=100,
        high=101,
        low=99,
        close=100.05,
        volume=100,
    )

    assert generate_candle_signal(candle) == Signal.HOLD

def test_rejects_negative_threshold_for_candle_signal():
    candle = Candle(
        timestamp=4,
        open=100,
        high=101,
        low=99,
        close=100.5,
        volume=100,
    )

    with pytest.raises(ValueError):
        generate_candle_signal(candle, -0.1)
