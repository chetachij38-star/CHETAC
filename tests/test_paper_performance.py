from src.trade import TradeResult
from src.paper_performance import build_paper_performance


def test_build_paper_performance():
    trades = [
        TradeResult(
            direction="long",
            entry_price=100,
            exit_price=105,
            position_size=1,
            net_result=5.0,
        ),
        TradeResult(
            direction="short",
            entry_price=105,
            exit_price=102,
            position_size=1,
            net_result=3.0,
        ),
        TradeResult(
            direction="long",
            entry_price=102,
            exit_price=100,
            position_size=1,
            net_result=-2.0,
        ),
    ]

    report = build_paper_performance(
        starting_balance=1000,
        trade_results=trades,
    )

    assert report.starting_balance == 1000
    assert report.ending_balance == 1006
    assert report.trades == 3
    assert report.total_return_percent == 0.6
    assert report.win_rate == (2 / 3) * 100
    assert report.profit_factor == 4.0
    assert report.equity_curve == [1000, 1005, 1008, 1006]
    assert report.max_drawdown == (2 / 1008) * 100
