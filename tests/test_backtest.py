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

def test_backtest_does_not_use_current_close_for_entry_signal():
    candles = [
        Candle(
            timestamp=1,
            open=100,
            high=100,
            low=100,
            close=100,
            volume=100,
        ),
        Candle(
            timestamp=2,
            open=100,
            high=120,
            low=100,
            close=120,
            volume=100,
        ),
        Candle(
            timestamp=3,
            open=120,
            high=120,
            low=120,
            close=120,
            volume=100,
        ),
    ]

    result = run_backtest(candles, 1000)

    assert result.ending_balance == 1000
    assert result.trades == 0


def test_mt5_candles_feed_backtest(monkeypatch):
    import src.mt5_market_data as mt5_market_data

    class FakeMT5:
        TIMEFRAME_H1 = "H1"

        def initialize(self):
            return True

        def copy_rates_from_pos(self, symbol, timeframe, start_pos, count):
            assert symbol == "XAUUSD.m"
            assert timeframe == self.TIMEFRAME_H1
            assert start_pos == 0
            assert count == 3

            return [
                {
                    "time": 1790100000,
                    "open": 100,
                    "high": 101,
                    "low": 99,
                    "close": 100,
                    "tick_volume": 1000,
                },
                {
                    "time": 1790103600,
                    "open": 101,
                    "high": 102,
                    "low": 100,
                    "close": 101,
                    "tick_volume": 1100,
                },
                {
                    "time": 1790107200,
                    "open": 102,
                    "high": 103,
                    "low": 101,
                    "close": 102,
                    "tick_volume": 1200,
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
        3,
    )

    result = run_backtest(candles, 1000)

    assert result.starting_balance == 1000
    assert result.ending_balance == 1002
    assert result.trades == 2

