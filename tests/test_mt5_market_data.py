from src.market_data import Candle
from src.mt5_market_data import candle_from_mt5


def test_candle_from_mt5():
    raw_candle = {
        "time": 1790100000,
        "open": 4330.10,
        "high": 4340.50,
        "low": 4325.20,
        "close": 4336.40,
        "tick_volume": 12500,
    }

    candle = candle_from_mt5(raw_candle)

    assert isinstance(candle, Candle)
    assert candle.timestamp == 1790100000
    assert candle.open == 4330.10
    assert candle.high == 4340.50
    assert candle.low == 4325.20
    assert candle.close == 4336.40
    assert candle.volume == 12500
