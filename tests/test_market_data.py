import pytest

from src.market_data import Candle


def test_valid_candle():
    candle = Candle(
        timestamp=1000,
        open=100,
        high=105,
        low=95,
        close=103,
        volume=500,
    )

    assert candle.close == 103
    assert candle.high == 105
    assert candle.low == 95


def test_rejects_invalid_price():
    with pytest.raises(ValueError):
        Candle(1000, 0, 105, 95, 103, 500)


def test_rejects_invalid_high():
    with pytest.raises(ValueError):
        Candle(1000, 100, 99, 95, 103, 500)


def test_rejects_negative_volume():
    with pytest.raises(ValueError):
        Candle(1000, 100, 105, 95, 103, -1)
