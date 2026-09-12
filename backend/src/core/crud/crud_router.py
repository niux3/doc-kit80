from typing import Type, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel, Session
from src.core.crud.abstract_crud import AbstractCRUD
from src.core.database import db


class CRUDRouter:
    def __init__(
        self,
        crud_service: AbstractCRUD,
        create_schema: Type[SQLModel],
        read_schema: Type[SQLModel],
        update_schema: Type[SQLModel],
        prefix: str,
        tags: Optional[List[str]] = None,
    ):
        self.service = crud_service
        self.create_schema = create_schema
        self.read_schema = read_schema
        self.update_schema = update_schema

        default_tag = tags or [
            read_schema.__name__.replace("Read", "").lower()
        ]

        self.router = APIRouter(
            prefix=prefix,
            tags=default_tag
        )
        self._register_routes()

    def _register_routes(self):
        create_schema = self.create_schema
        read_schema = self.read_schema
        update_schema = self.update_schema
        entity_name = read_schema.__name__.replace("Read", "")

        @self.router.get("/", response_model=List[read_schema])
        def get_all(session: Session = Depends(db.get_session)):
            return self.service.get_all(session)

        @self.router.get("/{id}", response_model=read_schema)
        def get_one(id: int | str, session: Session = Depends(db.get_session)):
            item = self.service.get_one(session, id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{entity_name} {id} not found"
                )
            return item

        @self.router.post("/", response_model=read_schema, status_code=status.HTTP_201_CREATED)
        def create(payload: create_schema, session: Session = Depends(db.get_session)):
            return self.service.create(session, payload)

        @self.router.put("/{id}", response_model=read_schema)
        def update(id: int | str, payload: update_schema, session: Session = Depends(db.get_session)):
            item = self.service.update(session, id, payload)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{entity_name} {id} not found"
                )
            return item

        @self.router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
        def destroy(id: int | str, session: Session = Depends(db.get_session)):
            success = self.service.destroy(session, id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{entity_name} {id} not found"
                )
            return None
