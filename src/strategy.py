from enum import Enum


class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


def generate_signal(
    fast_price: float,
    slow_price: float,
    minimum_difference_percent: float = 0.1,
) -> Signal:
    """Generate a basic price-momentum signal."""

    if fast_price <= 0 or slow_price <= 0:
        raise ValueError("Prices must be greater than zero.")

    if minimum_difference_percent < 0:
        raise ValueError("Minimum difference cannot be negative.")

    difference_percent = ((fast_price - slow_price) / slow_price) * 100

    if difference_percent >= minimum_difference_percent:
        return Signal.BUY

    if difference_percent <= -minimum_difference_percent:
        return Signal.SELL

    return Signal.HOLD
