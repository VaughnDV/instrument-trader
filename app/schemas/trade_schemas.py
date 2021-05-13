from typing import Optional
import datetime as dt
from pydantic import BaseModel, Field
from app.models.trade_models import AssetClassEnum, TradeBuySellEnum


class TradeDetails(BaseModel):
    buy_sell_indicator: TradeBuySellEnum = Field(
        description="A value of BUY for buys, SELL for sells."
    )
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")

    class Config:
        orm_mode = True


class Instrument(BaseModel):
    id: str = Field(
        alias="id",
        description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc",
    )
    name: str = Field(alias="name", description="The name of the instrument traded.")

    class Config:
        orm_mode = True


class Trader(BaseModel):
    id: str = Field(
        alias="id",
        description="The ID of the trader",
    )
    name: str = Field(description="The name of the Trader")

    class Config:
        orm_mode = True


class Trade(BaseModel):
    asset_class: AssetClassEnum = Field(
        alias="asset_class",
        default=None,
        description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc",
    )

    counterparty: Optional[str] = Field(
        default=None,
        description="The counterparty the trade was executed with. May not always be available",
    )
    instrument: Instrument
    trade_date_time: dt.datetime = Field(
        alias="trade_date_time", description="The date-time the Trade was executed"
    )
    trade_details: TradeDetails = Field(
        alias="trade_detail",
        description="The details of the trade, i.e. price, quantity",
    )
    trade_id: str = Field(
        alias="trade_id", default=None, description="The unique ID of the trade"
    )

    trader: Trader = Field(description="The name of the Trader")

    class Config:
        orm_mode = True
