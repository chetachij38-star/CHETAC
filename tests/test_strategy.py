import pytest

from src.strategy import Signal, generate_signal


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


def test_generates_buy_signal_from_completed_candle():
    assert generate_signal(102, 100) == Signal.BUY

