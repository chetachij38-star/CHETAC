import pytest

from src.risk import calculate_position_size


def test_position_size_calculation():
    result = calculate_position_size(
        account_balance=1000,
        risk_percent=1,
        entry_price=100,
        stop_loss_price=95,
    )

    assert result == pytest.approx(2.0)


def test_rejects_zero_balance():
    with pytest.raises(ValueError):
        calculate_position_size(0, 1, 100, 95)


def test_rejects_equal_entry_and_stop_loss():
    with pytest.raises(ValueError):
        calculate_position_size(1000, 1, 100, 100)
