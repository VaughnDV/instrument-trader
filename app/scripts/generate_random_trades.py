import random

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import trade_models


DUMMY_TRADERS = [{"name": "bob smith"}, {"name": "joe blob"}, {"name": "john doe"}]

DUMMY_INSTRUMENTS = [
    {"id": "TSLA", "name": "Tesla"},
    {"id": "AAPL", "name": "Apple"},
    {"id": "AMZN", "name": "Amazon"},
]


def generate(db: Session, number_of_trades: int = 10) -> None:

    for trader in DUMMY_TRADERS:
        try:
            db_trader = trade_models.Trader(**trader)
            db.add(db_trader)
            db.commit()
            db.refresh(db_trader)
        except IntegrityError:
            db.rollback()
            continue

    for instrument in DUMMY_INSTRUMENTS:
        try:
            db_instrument = trade_models.Instrument(**instrument)
            db.add(db_instrument)
            db.commit()
            db.refresh(db_instrument)
        except IntegrityError:
            db.rollback()
            continue

    for i in range(number_of_trades):
        db_trade_detail = trade_models.TradeDetail(
            buy_sell_indicator=random.choice(["BUY", "SELL"]),
            price=float(random.randint(100, 1000000)) / 100,
            quantity=random.randint(1, 100),
        )
        db_trader = random.choice(
            db.query(trade_models.Trader)
            .all()
        )
        db_instrument = random.choice(
            db.query(trade_models.Instrument)
            .all()
        )
        db.add(db_trade_detail)
        db.commit()
        db.refresh(db_trade_detail)

        db_trade = trade_models.Trade(
            asset_class=random.choice(["FX", "EQUITY", "BOND"]),
            counterparty=random.choice(["StockTrader", "Jeff", "Elon", ""]),
            trade_detail=db_trade_detail,
            trader=db_trader,
            instrument=db_instrument,
        )
        db.add(db_trade)

    db.commit()
    return True
