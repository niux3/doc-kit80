from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any


ModelType = TypeVar("ModelType")
CreateType = TypeVar("CreateType")
ReadType = TypeVar("ReadType")
UpdateType = TypeVar("UpdateType")


class AbstractCRUD(ABC, Generic[ModelType, CreateType, ReadType, UpdateType]):
    @abstractmethod
    def get_all(self, db_context: Any) -> List[ModelType]:
        ...

    @abstractmethod
    def get_one(self, db_context: Any, id: int | str) -> Optional[ModelType]:
        ...

    @abstractmethod
    def create(self, db_context: Any, payload: CreateType) -> ModelType:
        ...

    @abstractmethod
    def update(self, db_context: Any, id: int | str, payload: UpdateType) -> ModelType:
        ...

    @abstractmethod
    def destroy(self, db_context: Any, id: int | str) -> bool:
        ...
