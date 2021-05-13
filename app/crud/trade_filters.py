from sqlalchemy.orm import Session
from app.models import trade_models
from typing import List
from app.types import ModelType


def search_filter_by_counterparty(db: Session, search_value: str) -> List[ModelType]:
    result = (
        db.query(trade_models.Trade)
        .filter(trade_models.Trade.counterparty == search_value)
        .all()
    )
    return result


def search_filter_by_instrument(db: Session, search_value: str) -> List[ModelType]:
    result = (
        db.query(trade_models.Trade)
        .join(trade_models.Trade.instrument)
        .filter(trade_models.Instrument.name == search_value)
        .all()
    )
    if not result:
        result = (
            db.query(trade_models.Trade)
            .join(trade_models.Trade.instrument)
            .filter(trade_models.Instrument.id == search_value)
            .all()
        )
    return result


def search_filter_by_trader_name(db: Session, search_value: str) -> List[ModelType]:
    result = (
        db.query(trade_models.Trade)
        .join(trade_models.Trade.trader)
        .filter(trade_models.Trader.name == search_value)
        .all()
    )
    return result


def filter_by_asset_class(db: Session, values_dict: dict) -> List[ModelType]:
    asset_classes = values_dict["asset_class"].split(",")
    return (
        db.query(trade_models.Trade)
        .filter(trade_models.Trade.asset_class.in_(asset_classes))
        .all()
    )


def filter_by_trade_date(db: Session, values_dict: dict) -> List[ModelType]:
    start = values_dict["start"]
    end = values_dict["end"]

    if end and not start:
        return (
            db.query(trade_models.Trade)
            .filter(trade_models.Trade.trade_date_time <= end)
            .all()
        )

    if start and not end:
        return (
            db.query(trade_models.Trade)
            .filter(trade_models.Trade.trade_date_time >= start)
            .all()
        )

    return (
        db.query(trade_models.Trade)
        .filter(trade_models.Trade.trade_date_time <= start)
        .filter(trade_models.Trade.trade_date_time >= end)
        .all()
    )


def filter_by_price(db: Session, values_dict: dict) -> List[ModelType]:
    max_price = float(values_dict["max_price"])
    min_price = float(values_dict["min_price"])

    if max_price and not min_price:
        return (
            db.query(trade_models.Trade)
            .join(trade_models.Trade.trade_detail)
            .filter(trade_models.TradeDetail.price <= max_price)
            .all()
        )

    if min_price and not max_price:
        return (
            db.query(trade_models.Trade)
            .join(trade_models.Trade.trade_detail)
            .filter(trade_models.TradeDetail.price >= min_price)
            .all()
        )

    return (
        db.query(trade_models.Trade)
        .join(trade_models.Trade.trade_detail)
        .filter(trade_models.TradeDetail.price <= max_price)
        .filter(trade_models.TradeDetail.price >= min_price)
        .all()
    )


def filter_by_buy_sell_indicator(db: Session, trade_type: str) -> List[ModelType]:
    return (
        db.query(trade_models.Trade)
        .join(trade_models.Trade.trade_detail)
        .filter(trade_models.TradeDetail.buy_sell_indicator == trade_type)
        .all()
    )
