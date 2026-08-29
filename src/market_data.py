from dataclasses import dataclass


@dataclass(frozen=True)
class Candle:
    """Represents one OHLCV market candle."""

    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self):
        if self.timestamp < 0:
            raise ValueError("Timestamp cannot be negative.")

        if self.open <= 0:
            raise ValueError("Open price must be greater than zero.")

        if self.high <= 0:
            raise ValueError("High price must be greater than zero.")

        if self.low <= 0:
            raise ValueError("Low price must be greater than zero.")

        if self.close <= 0:
            raise ValueError("Close price must be greater than zero.")

        if self.volume < 0:
            raise ValueError("Volume cannot be negative.")

        if self.high < max(self.open, self.close):
            raise ValueError("High price must be at least the open and close.")

        if self.low > min(self.open, self.close):
            raise ValueError("Low price must be at most the open and close.")

        if self.low > self.high:
            raise ValueError("Low price cannot be greater than high price.")
