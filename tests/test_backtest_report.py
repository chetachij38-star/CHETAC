import pytest

from src.backtest import build_backtest_report


def test_backtest_report_contains_key_metrics():
    report = build_backtest_report(
        starting_balance=1000,
        trade_results=[100, -50, 75, -25],
    )

    assert report.starting_balance == 1000
    assert report.ending_balance == 1100
    assert report.total_return_percent == pytest.approx(10.0)
    assert report.trades == 4
    assert report.win_rate == pytest.approx(50.0)
    assert report.max_drawdown > 0
    assert report.equity_curve == [1000, 1100, 1050, 1125, 1100]


def test_report_with_no_trades():
    report = build_backtest_report(
        starting_balance=1000,
        trade_results=[],
    )

    assert report.ending_balance == 1000
    assert report.trades == 0
    assert report.win_rate == 0.0
    assert report.equity_curve == [1000]


def test_report_rejects_invalid_balance():
    with pytest.raises(ValueError):
        build_backtest_report(
            starting_balance=0,
            trade_results=[100],
        )
