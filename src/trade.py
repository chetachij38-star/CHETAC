from dataclasses import dataclass


@dataclass(frozen=True)
class Trade:
    """Represents a proposed or completed trade."""

    direction: str
    entry_price: float
    exit_price: float
    position_size: float

    def __post_init__(self):
        if self.direction not in {"long", "short"}:
            raise ValueError("Direction must be 'long' or 'short'.")

        if self.entry_price <= 0:
            raise ValueError("Entry price must be greater than zero.")

        if self.exit_price <= 0:
            raise ValueError("Exit price must be greater than zero.")

        if self.position_size <= 0:
            raise ValueError("Position size must be greater than zero.")


@dataclass(frozen=True)
class TradeResult:
    """Represents the financial result of an executed trade."""

    direction: str
    entry_price: float
    exit_price: float
    position_size: float
    net_result: float

    def __post_init__(self):
        if self.direction not in {"long", "short"}:
            raise ValueError("Direction must be 'long' or 'short'.")

        if self.entry_price <= 0:
            raise ValueError("Entry price must be greater than zero.")

        if self.exit_price <= 0:
            raise ValueError("Exit price must be greater than zero.")

        if self.position_size <= 0:
            raise ValueError("Position size must be greater than zero.")
