from abc import ABC, abstractmethod
from typing import Callable


class GetMixin(ABC):
    @abstractmethod
    def get(self, search_id: int):
        ...


class GetListMixin(ABC):
    @abstractmethod
    def get_list(
        self,
        pagination_limit: int,
        pagination_offset: int,
        sort_key: str,
        sort_direction: str,
    ):
        ...


class SearchFiltersMixin(ABC):
    @abstractmethod
    def search(self, search_value: str):
        ...


class FiltersMixin(ABC):
    @abstractmethod
    def filter(self, filter_func: Callable, values_dict: dict):
        ...
