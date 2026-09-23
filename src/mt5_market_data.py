import MetaTrader5 as mt5

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


def get_mt5_candles(symbol: str, timeframe, count: int) -> list[Candle]:
    """Retrieve historical MT5 candles and convert them to CHETAC Candles."""

    if not symbol:
        raise ValueError("Symbol cannot be empty.")

    if count <= 0:
        raise ValueError("Count must be greater than zero.")

    if not mt5.initialize():
        raise RuntimeError(
            f"MT5 initialization failed: {mt5.last_error()}"
        )

    try:
        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            0,
            count,
        )

        if rates is None:
            raise RuntimeError(
                f"MT5 historical data request failed: {mt5.last_error()}"
            )

        return [candle_from_mt5(rate) for rate in rates]

    finally:
        mt5.shutdown()
