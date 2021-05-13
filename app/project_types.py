from typing import TypeVar
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)