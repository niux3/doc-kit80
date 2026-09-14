from typing import Type, TypeVar, List, Optional
from sqlmodel import SQLModel, Session
from src.core.crud.abstract_crud import AbstractCRUD

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateType = TypeVar("CreateType", bound=SQLModel)
ReadType = TypeVar("ReadType", bound=SQLModel)
UpdateType = TypeVar("UpdateType", bound=SQLModel)


class SQLModelCRUD(AbstractCRUD[ModelType, CreateType, ReadType, UpdateType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, session: Session) -> List[ModelType]:
        return session.query(self.model).all()

    def get_one(self, session: Session, id: int | str) -> Optional[ModelType]:
        # item = session.query(self.model).get(id)
        item = session.get(self.model, id)
        if not item:
            return None
        return item

    def create(self, session: Session, payload: CreateType) -> ModelType:
        db_obj = self.model.model_validate(payload.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(self, session: Session, id: int | str, payload: UpdateType) -> Optional[ModelType]:
        item = self.get_one(session, id)
        if not item:
            return None
        data = payload.model_dump(exclude_unset=True)
        item.sqlmodel_update(data)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    def destroy(self, session: Session, id: int | str) -> bool:
        item = self.get_one(session, id)
        if not item:
            return False
        session.delete(item)
        session.commit()
        return True
