def calculate_net_trade_result(
    entry_price: float,
    exit_price: float,
    position_size: float,
    fee_rate: float,
    slippage_per_unit: float,
) -> float:
    """Calculate net trade result after slippage and trading fees."""

    if entry_price <= 0 or exit_price <= 0:
        raise ValueError("Prices must be greater than zero.")

    if position_size <= 0:
        raise ValueError("Position size must be greater than zero.")

    if fee_rate < 0:
        raise ValueError("Fee rate cannot be negative.")

    if slippage_per_unit < 0:
        raise ValueError("Slippage cannot be negative.")

    adjusted_entry = entry_price + slippage_per_unit
    adjusted_exit = exit_price - slippage_per_unit

    gross_result = (adjusted_exit - adjusted_entry) * position_size

    entry_value = adjusted_entry * position_size
    exit_value = adjusted_exit * position_size

    fees = (entry_value + exit_value) * fee_rate

    return gross_result - fees
