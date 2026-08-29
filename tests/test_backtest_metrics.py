import pytest

from src.backtest import calculate_max_drawdown, calculate_profit_factor


def test_max_drawdown():
    equity = [1000, 1100, 1050, 900, 950]

    assert calculate_max_drawdown(equity) == pytest.approx(18.181818, rel=1e-5)


def test_no_drawdown_when_equity_only_rises():
    equity = [1000, 1050, 1100]

    assert calculate_max_drawdown(equity) == pytest.approx(0.0)


def test_profit_factor():
    profits = [100, 50]
    losses = [-40, -10]

    assert calculate_profit_factor(profits, losses) == pytest.approx(3.0)


def test_profit_factor_with_no_losses():
    assert calculate_profit_factor([100], []) == float("inf")


def test_profit_factor_with_no_profits():
    assert calculate_profit_factor([], [-100]) == 0.0
