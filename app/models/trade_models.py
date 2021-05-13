from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Float, DateTime, func
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class Trader(Base):
    __tablename__ = 'trader'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    trade = relationship("Trade", back_populates="trader")


class Instrument(Base):
    __tablename__ = 'instrument'
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    trade = relationship("Trade", back_populates="instrument")


class TradeBuySellEnum(enum.Enum):
    BUY = "buy"
    SELL = "sell"


class AssetClassEnum(enum.Enum):
    BOND = "bond"
    EQUITY = "equity"
    FX = "fx"


class TradeDetail(Base):
    __tablename__ = 'trade_detail'

    id = Column(Integer, primary_key=True, index=True)
    buy_sell_indicator = Column(Enum(TradeBuySellEnum), nullable=False)
    price = Column(Float(precision=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    trade = relationship("Trade", uselist=False, back_populates="trade_detail")


class Trade(Base):
    __tablename__ = 'trade'

    trade_id = Column(Integer, primary_key=True, index=True)
    asset_class = Column(Enum(AssetClassEnum), nullable=False)
    counterparty = Column(String, nullable=True)
    trade_date_time = Column(DateTime, default=func.now())

    # One to One with TradeDetail
    trade_detail_id = Column(Integer, ForeignKey('trade_detail.id'))
    trade_detail = relationship("TradeDetail", back_populates="trade")

    # Many to One with Instrument
    instrument_id = Column(Integer, ForeignKey("instrument.id"))
    instrument = relationship("Instrument", back_populates="trade")

    # Many to One with Trader
    trader_id = Column(Integer, ForeignKey("trader.name"))
    trader = relationship("Trader", back_populates="trade")
