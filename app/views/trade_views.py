from typing import List, Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.models import trade_models
from app.crud import trade_crud, trade_filters
from app.schemas import trade_schemas
from app.database import engine, get_db

router = APIRouter()
trade_models.Base.metadata.create_all(bind=engine)


@router.get("/trades/", response_model=List[trade_schemas.Trade])
def trades_list_view(
    search: Optional[str] = None,
    asset_class: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    trade_type: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    sort_direction: str = "asc",
    sort_key: str = "trade_id",
    db: Session = Depends(get_db)
):
    """
    A view for listing trades, supports pagination, sorting, search and filtering
    """
    service = trade_crud.TradeCRUDService(db)

    if search:
        return service.search_filters(search)

    if asset_class:
        return service.filter_list(trade_filters.filter_by_asset_class, dict(asset_class=asset_class))
    if start or end:
        return service.filter_list(trade_filters.filter_by_trade_date, dict(start=start, end=end))
    if max_price or min_price:
        return service.filter_list(trade_filters.filter_by_price, dict(max_price=max_price, enmin_priced=min_price))
    if trade_type:
        return service.filter_list(trade_filters.filter_by_price, dict(max_price=max_price, enmin_priced=min_price))

    return service.get_list(
        pagination_offset=offset,
        pagination_limit=limit,
        sort_key=sort_key,
        sort_direction=sort_direction
    )


@router.get("/trades/{trade_id}", response_model=trade_schemas.Trade)
def trade_detail_view(trade_id: int, db: Session = Depends(get_db)):
    """
    A view for retrieving a single trade detail by trade_id
    """
    service = trade_crud.TradeCRUDService(db)
    db_trade = service.get(trade_id)
    if db_trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_trade
