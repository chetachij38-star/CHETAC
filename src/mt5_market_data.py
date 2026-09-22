from src.market_data import Candle


def candle_from_mt5(raw_candle) -> Candle:
    """Convert one MT5 OHLC candle into a CHETAC Candle."""

    return Candle(
        timestamp=int(raw_candle["time"]),
        open=float(raw_candle["open"]),
        high=float(raw_candle["high"]),
        low=float(raw_candle["low"]),
        close=float(raw_candle["close"]),
        volume=float(raw_candle["tick_volume"]),
    )
