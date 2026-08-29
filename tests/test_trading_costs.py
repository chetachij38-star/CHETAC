import pytest

from src.backtest import calculate_position_size, calculate_trade_cost


def test_position_size_from_risk():
    size = calculate_position_size(
        balance=1000,
        risk_percent=1,
        entry_price=100,
        stop_loss_price=95,
    )

    assert size == pytest.approx(2.0)


def test_trade_cost():
    cost = calculate_trade_cost(
        position_size=2,
        entry_price=100,
        exit_price=110,
        fee_rate=0.001,
        slippage_rate=0.0005,
    )

    assert cost > 0


def test_rejects_invalid_risk_percent():
    with pytest.raises(ValueError):
        calculate_position_size(1000, 0, 100, 95)


def test_rejects_invalid_fee_rate():
    with pytest.raises(ValueError):
        calculate_trade_cost(2, 100, 110, -0.001, 0.0005)
