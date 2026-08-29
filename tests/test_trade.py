from src.trade import Trade, TradeResult


def test_trade_stores_trade_details():
    trade = Trade(
        direction="long",
        entry_price=100,
        exit_price=105,
        position_size=2,
    )

    assert trade.direction == "long"
    assert trade.entry_price == 100
    assert trade.exit_price == 105
    assert trade.position_size == 2


def test_trade_result_calculates_profit():
    result = TradeResult(
        direction="long",
        entry_price=100,
        exit_price=105,
        position_size=2,
        net_result=9.5,
    )

    assert result.net_result == 9.5


def test_trade_rejects_invalid_direction():
    import pytest

    with pytest.raises(ValueError):
        Trade(
            direction="invalid",
            entry_price=100,
            exit_price=105,
            position_size=2,
        )
