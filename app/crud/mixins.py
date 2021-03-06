from abc import ABC, abstractmethod
from typing import Callable, List

from sqlalchemy.orm import Session

from app.custom_types import ModelType


class GetMixin(ABC):
    db: Session
    model: ModelType

    def get(self, search_id: int) -> ModelType:
        return (
            self.db.query(self.model).filter(self.model.id == search_id).first()
        )


class GetListMixin(ABC):
    db: Session
    model: ModelType

    def get_list(self) -> ModelType:
        return self.db.query(self.model).all()


class SearchFiltersMixin(ABC):

    @abstractmethod
    def search(self, search_value: str) -> List[ModelType]:
        ...


class FiltersMixin(ABC):
    db: Session

    def filter(self, filter_fn: Callable, values_dict: dict) -> List[ModelType]:
        return filter_fn(self.db, values_dict)
