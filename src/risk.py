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


def validate_exposure(
    account_balance: float,
    position_value: float,
    max_exposure_percent: float,
) -> bool:
    """Check whether a position stays within the account exposure limit."""

    if account_balance <= 0:
        raise ValueError("Account balance must be greater than zero.")

    if position_value < 0:
        raise ValueError("Position value cannot be negative.")

    if max_exposure_percent <= 0:
        raise ValueError("Maximum exposure percent must be greater than zero.")

    exposure_percent = (position_value / account_balance) * 100

    return exposure_percent <= max_exposure_percent


def calculate_stop_loss(
    entry_price: float,
    risk_percent: float,
    direction: str,
) -> float:
    """Calculate a stop-loss price from entry price and risk percentage."""

    if entry_price <= 0:
        raise ValueError("Entry price must be greater than zero.")

    if risk_percent <= 0:
        raise ValueError("Risk percent must be greater than zero.")

    if direction not in {"long", "short"}:
        raise ValueError("Direction must be 'long' or 'short'.")

    risk_amount = entry_price * (risk_percent / 100)

    if direction == "long":
        return entry_price - risk_amount

    return entry_price + risk_amount


def calculate_risk_position_size(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float,
) -> float:
    """Calculate position size based on maximum account risk."""

    if account_balance <= 0:
        raise ValueError("Account balance must be greater than zero.")

    if risk_percent <= 0:
        raise ValueError("Risk percent must be greater than zero.")

    if entry_price <= 0:
        raise ValueError("Entry price must be greater than zero.")

    if stop_loss_price <= 0:
        raise ValueError("Stop-loss price must be greater than zero.")

    risk_per_unit = abs(entry_price - stop_loss_price)

    if risk_per_unit == 0:
        raise ValueError("Entry and stop-loss prices must be different.")

    maximum_loss = account_balance * (risk_percent / 100)

    return maximum_loss / risk_per_unit


def check_daily_loss_limit(
    starting_day_balance: float,
    current_balance: float,
    max_daily_loss_percent: float,
) -> bool:
    """Return whether trading may continue within the daily loss limit."""

    if starting_day_balance <= 0:
        raise ValueError("Starting day balance must be greater than zero.")

    if current_balance < 0:
        raise ValueError("Current balance cannot be negative.")

    if max_daily_loss_percent <= 0:
        raise ValueError("Maximum daily loss percent must be greater than zero.")

    loss_percent = (
        (starting_day_balance - current_balance)
        / starting_day_balance
    ) * 100

    return loss_percent < max_daily_loss_percent
