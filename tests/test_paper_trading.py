from src.market_data import Candle
from src.paper_trading import run_paper_trading


def test_paper_trading_updates_account_balance():
    candles = [
        Candle(
            timestamp=1,
            open=100,
            high=101,
            low=99,
            close=100,
            volume=1000,
        ),
        Candle(
            timestamp=2,
            open=100,
            high=106,
            low=99,
            close=105,
            volume=1200,
        ),
    ]

    result = run_paper_trading(
        candles=candles,
        starting_balance=1000,
        risk_percent=1,
        max_exposure_percent=30,
        max_daily_loss_percent=5,
        fee_rate=0.001,
        slippage_per_unit=0.01,
    )

    assert result.starting_balance == 1000
    assert result.trades == 1
    assert result.ending_balance > 1000
