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
def test_get_mt5_candles(monkeypatch):
    import src.mt5_market_data as mt5_market_data

    class FakeMT5:
        TIMEFRAME_H1 = "H1"

        def initialize(self):
            return True

        def copy_rates_from_pos(self, symbol, timeframe, start_pos, count):
            assert symbol == "XAUUSD.m"
            assert timeframe == self.TIMEFRAME_H1
            assert start_pos == 0
            assert count == 2

            return [
                {
                    "time": 1790100000,
                    "open": 4330.10,
                    "high": 4340.50,
                    "low": 4325.20,
                    "close": 4336.40,
                    "tick_volume": 12500,
                },
                {
                    "time": 1790103600,
                    "open": 4336.40,
                    "high": 4345.00,
                    "low": 4332.10,
                    "close": 4342.00,
                    "tick_volume": 14000,
                },
            ]

        def last_error(self):
            return (1, "Success")

        def shutdown(self):
            pass

    monkeypatch.setattr(mt5_market_data, "mt5", FakeMT5())

    candles = mt5_market_data.get_mt5_candles(
        "XAUUSD.m",
        FakeMT5.TIMEFRAME_H1,
        2,
    )

    assert len(candles) == 2
    assert all(isinstance(candle, Candle) for candle in candles)
    assert candles[0].close == 4336.40
    assert candles[1].close == 4342.00


def test_get_mt5_candles_rejects_mt5_initialization_failure(monkeypatch):
    import src.mt5_market_data as mt5_market_data

    class FakeMT5:
        def initialize(self):
            return False

        def last_error(self):
            return (10001, "Initialization failed")

    monkeypatch.setattr(mt5_market_data, "mt5", FakeMT5())

    try:
        mt5_market_data.get_mt5_candles(
            "XAUUSD.m",
            "H1",
            2,
        )
    except RuntimeError as exc:
        assert "MT5 initialization failed" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError")


def test_get_mt5_candles_rejects_failed_historical_data_request(monkeypatch):
    import src.mt5_market_data as mt5_market_data

    class FakeMT5:
        def initialize(self):
            return True

        def copy_rates_from_pos(self, symbol, timeframe, start_pos, count):
            return None

        def last_error(self):
            return (10002, "Historical data request failed")

        def shutdown(self):
            pass

    monkeypatch.setattr(mt5_market_data, "mt5", FakeMT5())

    try:
        mt5_market_data.get_mt5_candles(
            "XAUUSD.m",
            "H1",
            2,
        )
    except RuntimeError as exc:
        assert "MT5 historical data request failed" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError")
