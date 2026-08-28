def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float,
) -> float:
    """Calculate position size from account risk and stop-loss distance."""

    if account_balance <= 0:
        raise ValueError("Account balance must be greater than zero.")

    if risk_percent <= 0:
        raise ValueError("Risk percent must be greater than zero.")

    if entry_price <= 0 or stop_loss_price <= 0:
        raise ValueError("Prices must be greater than zero.")

    if entry_price == stop_loss_price:
        raise ValueError("Entry and stop-loss prices cannot be equal.")

    risk_amount = account_balance * (risk_percent / 100)
    price_distance = abs(entry_price - stop_loss_price)

    return risk_amount / price_distance
