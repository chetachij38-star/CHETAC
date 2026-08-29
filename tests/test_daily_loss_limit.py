import pytest

from src.risk import check_daily_loss_limit


def test_allows_trading_below_daily_loss_limit():
    assert check_daily_loss_limit(
        starting_day_balance=1000,
        current_balance=980,
        max_daily_loss_percent=5,
    ) is True


def test_blocks_trading_at_daily_loss_limit():
    assert check_daily_loss_limit(
        starting_day_balance=1000,
        current_balance=950,
        max_daily_loss_percent=5,
    ) is False


def test_blocks_trading_above_daily_loss_limit():
    assert check_daily_loss_limit(
        starting_day_balance=1000,
        current_balance=900,
        max_daily_loss_percent=5,
    ) is False


def test_allows_profit():
    assert check_daily_loss_limit(
        starting_day_balance=1000,
        current_balance=1050,
        max_daily_loss_percent=5,
    ) is True


def test_rejects_invalid_starting_balance():
    with pytest.raises(ValueError):
        check_daily_loss_limit(
            starting_day_balance=0,
            current_balance=950,
            max_daily_loss_percent=5,
        )
