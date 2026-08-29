import pytest

from src.risk import calculate_stop_loss, calculate_risk_position_size


def test_calculates_long_stop_loss():
    assert calculate_stop_loss(
        entry_price=100,
        risk_percent=2,
        direction="long",
    ) == 98


def test_calculates_short_stop_loss():
    assert calculate_stop_loss(
        entry_price=100,
        risk_percent=2,
        direction="short",
    ) == 102


def test_calculates_position_size_from_account_risk():
    assert calculate_risk_position_size(
        account_balance=1000,
        risk_percent=2,
        entry_price=100,
        stop_loss_price=98,
    ) == 10


def test_rejects_invalid_direction():
    with pytest.raises(ValueError):
        calculate_stop_loss(
            entry_price=100,
            risk_percent=2,
            direction="sideways",
        )


def test_rejects_invalid_risk_percent():
    with pytest.raises(ValueError):
        calculate_stop_loss(
            entry_price=100,
            risk_percent=0,
            direction="long",
        )
