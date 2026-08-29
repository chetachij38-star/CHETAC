import pytest

from src.backtest import calculate_return_percent, calculate_win_rate


def test_calculate_return_percent():
    result = calculate_return_percent(1000, 1100)

    assert result == pytest.approx(10.0)


def test_calculate_negative_return():
    result = calculate_return_percent(1000, 900)

    assert result == pytest.approx(-10.0)


def test_calculate_win_rate():
    result = calculate_win_rate([100, 50, -25, -10])

    assert result == pytest.approx(50.0)


def test_all_winning_trades():
    result = calculate_win_rate([100, 50])

    assert result == pytest.approx(100.0)


def test_no_trades():
    result = calculate_win_rate([])

    assert result == pytest.approx(0.0)
