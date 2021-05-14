from abc import ABC, abstractmethod
from typing import Callable

from app.custom_types import ModelType


class GetMixin(ABC):
    @abstractmethod
    def get(self, search_id: int) -> ModelType:
        ...


class GetListMixin(ABC):
    @abstractmethod
    def get_list(
            self,
            pagination_limit: int,
            pagination_offset: int = 0,
            sort_key: str = "trade_id",
            sort_direction: str = "asc",
    ) -> ModelType:
        ...


class SearchFiltersMixin(ABC):
    @abstractmethod
    def search(self, search_value: str) -> ModelType:
        ...


class FiltersMixin(ABC):
    @abstractmethod
    def filter(self, filter_func: Callable, values_dict: dict) -> ModelType:
        ...
