from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.crud.mixins import GetMixin, GetListMixin, SearchFiltersMixin, FiltersMixin
from app.models import trade_models
from typing import List, Tuple, Callable
from app.custom_types import ModelType
from app.crud.trade_filters import (
    SearchFilter,
    SearchForInstrument,
    SearchForTraderName,
    SearchForCounterParty,
)


class TradeCRUDService(GetMixin, GetListMixin, SearchFiltersMixin, FiltersMixin):
    def __init__(
        self,
        db: Session = None,
        model: ModelType = trade_models.Trade,
        searchable_filters: Tuple[SearchFilter] = (
            SearchForInstrument(),
            SearchForTraderName(),
            SearchForCounterParty(),
        ),
    ):
        self.db = db
        self.model = model
        self.searchable_filters = searchable_filters

    def get_list(
        self,
        pagination_limit: int = 100,
        pagination_offset: int = 0,
        sort_key: str = "trade_id",
        sort_direction: str = "asc",
    ) -> List[ModelType]:
        sort = desc(sort_key) if sort_direction == "desc" else asc(sort_key)
        return (
            self.db.query(self.model)
            .order_by(sort)
            .offset(pagination_offset)
            .limit(pagination_limit)
            .all()
        )

    def get(self, search_id: int) -> ModelType:
        return (
            self.db.query(self.model).filter(self.model.trade_id == search_id).first()
        )
