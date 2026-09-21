from src.config import Instrument


def test_instrument_definition():
    instrument = Instrument(
        symbol="XAUUSD",
        name="Gold",
        asset_class="commodity",
    )

    assert instrument.symbol == "XAUUSD"
    assert instrument.name == "Gold"
    assert instrument.asset_class == "commodity"
