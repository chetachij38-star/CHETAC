import pytest

from src.backtest import build_equity_curve


def test_equity_curve_starts_with_starting_balance():
    result = build_equity_curve(1000, [100, -50, 25])

    assert result == [1000, 1100, 1050, 1075]


def test_equity_curve_with_no_trades():
    result = build_equity_curve(1000, [])

    assert result == [1000]


def test_equity_curve_handles_losses():
    result = build_equity_curve(1000, [-100, -50, 200])

    assert result == [1000, 900, 850, 1050]


def test_rejects_invalid_starting_balance():
    with pytest.raises(ValueError):
        build_equity_curve(0, [100])
