from src.risk import risk_gate


def test_risk_gate_allows_valid_trade():
    result = risk_gate(
        account_balance=1000,
        position_value=200,
        max_exposure_percent=30,
        starting_day_balance=1000,
        current_balance=990,
        max_daily_loss_percent=5,
    )

    assert result is True


def test_risk_gate_rejects_excessive_exposure():
    result = risk_gate(
        account_balance=1000,
        position_value=400,
        max_exposure_percent=30,
        starting_day_balance=1000,
        current_balance=990,
        max_daily_loss_percent=5,
    )

    assert result is False


def test_risk_gate_rejects_daily_loss_limit():
    result = risk_gate(
        account_balance=1000,
        position_value=200,
        max_exposure_percent=30,
        starting_day_balance=1000,
        current_balance=950,
        max_daily_loss_percent=5,
    )

    assert result is False
