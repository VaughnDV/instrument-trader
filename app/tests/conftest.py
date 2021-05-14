from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..main import app
from sqlalchemy.orm import Session
from ..models import trade_models

SQLALCHEMY_DATABASE_URL = "sqlite:///../test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db() -> Session:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


DUMMY_TRADERS = [{"name": "bob smith"}, {"name": "joe blob"}, {"name": "john doe"}]

DUMMY_INSTRUMENTS = [
    {"id": "TSLA", "name": "Tesla"},
    {"id": "AAPL", "name": "Apple"},
    {"id": "AMZN", "name": "Amazon"},
]

DUMMY_TRADES = [
    {
        "detail": {"buy_sell_indicator": "BUY", "price": 99.99, "quantity": 9},
        "trader": "bob smith",
        "instrument": "TSLA",
        "trade": {
            "asset_class": "BOND",
            "counterparty": "StockTrader",
        },
    },
    {
        "detail": {"buy_sell_indicator": "BUY", "price": 88.88, "quantity": 8},
        "trader": "joe blob",
        "instrument": "AAPL",
        "trade": {
            "asset_class": "EQUITY",
            "counterparty": "StockTrader",
        },
    },
    {
        "detail": {"buy_sell_indicator": "SELL", "price": 77.77, "quantity": 7},
        "trader": "john doe",
        "instrument": "AMZN",
        "trade": {
            "asset_class": "FX",
            "counterparty": "",
        },
    },
]


def setup_test_trades_data(db: Session = TestingSessionLocal()) -> None:
    for trader in DUMMY_TRADERS:
        db_trader = trade_models.Trader(**trader)
        db.add(db_trader)

    db.commit()

    for instrument in DUMMY_INSTRUMENTS:
        db_instrument = trade_models.Instrument(**instrument)
        db.add(db_instrument)

    db.commit()

    for trade in DUMMY_TRADES:
        db_trade_detail = trade_models.TradeDetail(**trade["detail"])
        db_trader = (
            db.query(trade_models.Trader)
            .filter(trade_models.Trader.name == trade["trader"])
            .first()
        )
        db_instrument = (
            db.query(trade_models.Instrument)
            .filter(trade_models.Instrument.id == trade["instrument"])
            .first()
        )
        db.add(db_trade_detail)
        db.commit()
        db_trade = trade_models.Trade(
            **trade["trade"],
            trade_detail=db_trade_detail,
            trader=db_trader,
            instrument=db_instrument,
        )
        db.add(db_trade)

    db.commit()

    return
