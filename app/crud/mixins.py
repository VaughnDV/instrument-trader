from abc import ABC
from typing import Callable, List, Tuple, Protocol

from sqlalchemy.orm import Session

from app.crud.trade_filters import SearchFilter, FilterAction
from app.custom_types import ModelType


class GetMixin(Protocol):
    db: Session
    model: ModelType

    def get(self, search_id: int) -> ModelType:
        """
        Query that fetches the first item from the database where the id matches the given search_id.
        Override this method if your id field is named something else
        """
        return self.db.query(self.model).filter(self.model.id == search_id).first()


class GetListMixin(Protocol):
    db: Session
    model: ModelType

    def get_list(self) -> List[ModelType]:
        """
        Query that fetches array of all results for the injected model
        """
        return self.db.query(self.model).all()


class SearchFiltersMixin(Protocol):
    db: Session
    model: ModelType
    searchable_filters: Tuple[SearchFilter]

    def search(self, search_value: str) -> List[ModelType]:
        """
        Iterates over the injected `searchable_filters`, compiles and then returns an array of results
        """
        results = []

        for searchable_filter_cls in self.searchable_filters:
            found: List[ModelType] = searchable_filter_cls.search(self.db, search_value)
            if found:
                results += found
        return results


class FiltersMixin(Protocol):
    db: Session
    model: ModelType

    def filter(self, filter_fn: FilterAction, values_dict: dict) -> List[ModelType]:
        """
        Calls the provided filter function using key, value pairs in `values_dict` and returns the results
        """
        return filter_fn(self.db, values_dict)
