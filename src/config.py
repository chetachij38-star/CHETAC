from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    """Defines a tradable market instrument."""

    symbol: str
    name: str
    asset_class: str
