import pytest

from src.execution import calculate_net_trade_result


def test_profitable_trade_after_fee_and_slippage():
    result = calculate_net_trade_result(
        entry_price=100,
        exit_price=110,
        position_size=2,
        fee_rate=0.001,
        slippage_per_unit=0.50,
    )

    assert result == pytest.approx(17.58)


def test_losing_trade_returns_negative_result():
    result = calculate_net_trade_result(
        entry_price=100,
        exit_price=90,
        position_size=2,
        fee_rate=0.001,
        slippage_per_unit=0.50,
    )

    assert result < 0


def test_rejects_invalid_position_size():
    with pytest.raises(ValueError):
        calculate_net_trade_result(
            entry_price=100,
            exit_price=110,
            position_size=0,
            fee_rate=0.001,
            slippage_per_unit=0.50,
        )


def test_rejects_negative_fee_rate():
    with pytest.raises(ValueError):
        calculate_net_trade_result(
            entry_price=100,
            exit_price=110,
            position_size=2,
            fee_rate=-0.001,
            slippage_per_unit=0.50,
        )
