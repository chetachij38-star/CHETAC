import pytest

from src.risk import validate_exposure


def test_accepts_position_within_exposure_limit():
    assert validate_exposure(
        account_balance=1000,
        position_value=200,
        max_exposure_percent=30,
    ) is True


def test_rejects_position_above_exposure_limit():
    assert validate_exposure(
        account_balance=1000,
        position_value=400,
        max_exposure_percent=30,
    ) is False


def test_accepts_position_at_exact_limit():
    assert validate_exposure(
        account_balance=1000,
        position_value=300,
        max_exposure_percent=30,
    ) is True


def test_rejects_invalid_balance():
    with pytest.raises(ValueError):
        validate_exposure(
            account_balance=0,
            position_value=100,
            max_exposure_percent=30,
        )


def test_rejects_invalid_limit():
    with pytest.raises(ValueError):
        validate_exposure(
            account_balance=1000,
            position_value=100,
            max_exposure_percent=0,
        )
