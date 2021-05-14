from .conftest import client, setup_test_trades_data
from datetime import datetime, timedelta

setup_test_trades_data()


def test_get_trade_by_id() -> None:
    response = client.get(
        "/trades/1",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(datetime.fromisoformat(data["trade_date_time"]), datetime)
    data.pop("trade_date_time")
    assert data == {
        "asset_class": "bond",
        "counterparty": "StockTrader",
        "instrument": {"id": "TSLA", "name": "Tesla"},
        "trade_detail": {"buy_sell_indicator": "buy", "price": 99.99, "quantity": 9},
        "trade_id": "1",
        "trader": {"id": "1", "name": "bob smith"},
    }


def test_list_traders() -> None:
    response = client.get(
        "/trades/",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    for d in data:
        d.pop("trade_date_time")
    assert data == [
        {
            "asset_class": "bond",
            "counterparty": "StockTrader",
            "instrument": {"id": "TSLA", "name": "Tesla"},
            "trade_detail": {
                "buy_sell_indicator": "buy",
                "price": 99.99,
                "quantity": 9,
            },
            "trade_id": "1",
            "trader": {"id": "1", "name": "bob smith"},
        },
        {
            "asset_class": "equity",
            "counterparty": "StockTrader",
            "instrument": {"id": "AAPL", "name": "Apple"},
            "trade_detail": {
                "buy_sell_indicator": "buy",
                "price": 88.88,
                "quantity": 8,
            },
            "trade_id": "2",
            "trader": {"id": "2", "name": "joe blob"},
        },
        {
            "asset_class": "fx",
            "counterparty": "",
            "instrument": {"id": "AMZN", "name": "Amazon"},
            "trade_detail": {
                "buy_sell_indicator": "sell",
                "price": 77.77,
                "quantity": 7,
            },
            "trade_id": "3",
            "trader": {"id": "3", "name": "john doe"},
        },
    ]


def test_search_trades_by_counterparty() -> None:
    response = client.get(
        "/trades/?search=StockTrader",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    for d in data:
        assert d["counterparty"] == "StockTrader"


def test_search_trades_by_instrument_id() -> None:
    response = client.get(
        "/trades/?search=TSLA",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    for d in data:
        assert d["instrument"]["id"] == "TSLA"


def test_search_trades_by_instrument_name() -> None:
    response = client.get(
        "/trades/?search=Tesla",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    for d in data:
        assert d["instrument"]["name"] == "Tesla"


def test_search_trades_by_trader() -> None:
    response = client.get(
        "/trades/?search=bob%20smith",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    for d in data:
        assert d["trader"]["name"] == "bob smith"


def test_filter_trades_by_asset_class() -> None:
    response = client.get(
        "/trades/?asset_class=EQUITY",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    for d in data:
        assert d["asset_class"] == "equity"


def test_filtering_on_multiple_asset_classes() -> None:
    response = client.get(
        "/trades/?asset_class=EQUITY,FX",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    assert data[0]["asset_class"] == "equity"
    assert data[1]["asset_class"] == "fx"


def test_filter_trades_before_end_date() -> None:
    date = str((datetime.now() + timedelta(days=1)).date())

    response = client.get(
        f"/trades/?end={date}",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    for d in data:
        assert d["trade_date_time"] < date


def test_filter_trades_before_end_date_returns_none() -> None:
    date = str((datetime.now() - timedelta(days=1)).date())

    response = client.get(
        f"/trades/?end={date}",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert not data


def trade_filer_trades_by_max_price() -> None:
    response = client.get(
        "/trades/?max_price=90",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    for d in data:
        assert d["trade_detail"]["price"] <= 90


def trade_filer_trades_by_min_price() -> None:
    response = client.get(
        "/trades/?min_price=80",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    for d in data:
        assert d["trade_detail"]["price"] >= 80


def trade_filer_trades_between_min_price_and_max_price() -> None:
    response = client.get(
        "/trades/?max_price=90&min_price=80",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    for d in data:
        assert 90 <= d["trade_detail"]["price"] >= 80


def trade_filter_trades_buy_sell_indicator() -> None:
    response = client.get(
        "/trades/?trade_type=BUY",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    for d in data:
        assert d["trade_detail"]["buy_sell_indicator"] == "buy"


def test_list_trades_pagination() -> None:
    response = client.get(
        "/trades/?offset=1&limit=1",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    data[0].pop("trade_date_time")
    assert data[0] == {
        "asset_class": "equity",
        "counterparty": "StockTrader",
        "instrument": {"id": "AAPL", "name": "Apple"},
        "trade_detail": {"buy_sell_indicator": "buy", "price": 88.88, "quantity": 8},
        "trade_id": "2",
        "trader": {"id": "2", "name": "joe blob"},
    }


def test_list_trades_sorting() -> None:
    response = client.get(
        "/trades/?sort_direction=desc",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    for d in data:
        d.pop("trade_date_time")
    assert data == [
        {
            "asset_class": "fx",
            "counterparty": "",
            "instrument": {"id": "AMZN", "name": "Amazon"},
            "trade_detail": {
                "buy_sell_indicator": "sell",
                "price": 77.77,
                "quantity": 7,
            },
            "trade_id": "3",
            "trader": {"id": "3", "name": "john doe"},
        },
        {
            "asset_class": "equity",
            "counterparty": "StockTrader",
            "instrument": {"id": "AAPL", "name": "Apple"},
            "trade_detail": {
                "buy_sell_indicator": "buy",
                "price": 88.88,
                "quantity": 8,
            },
            "trade_id": "2",
            "trader": {"id": "2", "name": "joe blob"},
        },
        {
            "asset_class": "bond",
            "counterparty": "StockTrader",
            "instrument": {"id": "TSLA", "name": "Tesla"},
            "trade_detail": {
                "buy_sell_indicator": "buy",
                "price": 99.99,
                "quantity": 9,
            },
            "trade_id": "1",
            "trader": {"id": "1", "name": "bob smith"},
        },
    ]
