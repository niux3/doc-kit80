from src.documentation.models import Language, LanguageCreate, LanguageRead, LanguageUpdate
from src.crud.base_router import CRUDRouter
from typing import Type, TypeVar, Generic, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel, Session, select
from src.database import db

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateType = TypeVar("CreateType", bound=SQLModel)
ReadType = TypeVar("ReadType", bound=SQLModel)
UpdateType = TypeVar("UpdateType", bound=SQLModel)


class CRUDRouter(Generic[ModelType, CreateType, ReadType, UpdateType]):
    def __init__(
        self,
        model: Type[ModelType],
        create_schema: Type[CreateType],
        read_schema: Type[ReadType],
        update_schema: Type[UpdateType],
        prefix: str,
        tags: Optional[List[str]] = None,
    ):
        self.model = model
        self.create_schema = create_schema
        self.read_schema = read_schema
        self.update_schema = update_schema

        # Instanciation du router propre à cette entité
        self.router = APIRouter(prefix=prefix, tags=tags or [
                                model.__name__.lower()])

        # Enregistrement dynamique des méthodes comme handlers HTTP
        self._register_routes()

    def _register_routes(self):
        self.router.add_api_route(
            "/",
            self.get_all,
            methods=["GET"],
            response_model=List[self.read_schema],
            summary=f"Récupérer tous les {self.model.__name__}",
        )
        self.router.add_api_route(
            "/{id}",
            self.get_one,
            methods=["GET"],
            response_model=self.read_schema,
            summary=f"Récupérer un {self.model.__name__} par son ID",
        )
        self.router.add_api_route(
            "/",
            self.create,
            methods=["POST"],
            response_model=self.read_schema,
            status_code=status.HTTP_201_CREATED,
            summary=f"Créer un {self.model.__name__}",
        )
        self.router.add_api_route(
            "/{id}",
            self.update,
            methods=["PUT"],
            response_model=self.read_schema,
            summary=f"Modifier un {self.model.__name__}",
        )
        self.router.add_api_route(
            "/{id}",
            self.destroy,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            summary=f"Supprimer un {self.model.__name__}",
        )

    # --- Handlers de base (surchargeables par héritage) ---

    def get_all(self, session: Session = Depends(db.get_session)):
        statement = select(self.model)
        return session.exec(statement).all()

    def get_one(self, id: int, session: Session = Depends(db.get_session)):
        item = session.get(self.model, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} {id} not found",
            )
        return item

    def create(self, payload: SQLModel, session: Session = Depends(db.get_session)):
        # On utilise Pydantic pour valider selon le schéma de création de l'instance
        validated_payload = self.create_schema.model_validate(payload)
        db_obj = self.model.model_validate(validated_payload.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(self, id: int, payload: SQLModel, session: Session = Depends(db.get_session)):
        item = session.get(self.model, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} {id} not found",
            )
        validated_payload = self.update_schema.model_validate(payload)
        data = validated_payload.model_dump(exclude_unset=True)
        item.sqlmodel_update(data)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    def destroy(self, id: int, session: Session = Depends(db.get_session)):
        item = session.get(self.model, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} {id} not found",
            )
        session.delete(item)
        session.commit()
        return None


# exemple

# Instanciation directe du router
language_crud = CRUDRouter(
    model=Language,
    create_schema=LanguageCreate,
    read_schema=LanguageRead,
    update_schema=LanguageUpdate,
    prefix="/language",
    tags=["language"],
)

# On exporte le router FastAPI généré
language_router = language_crud.router


# avec Auth
def _register_routes(self):
    # GET public
    self.router.add_api_route(
        "/",
        self.get_all,
        methods=["GET"],
        response_model=List[self.read_schema],
    )

    # POST protégé
    self.router.add_api_route(
        "/",
        self.create,
        methods=["POST"],
        response_model=self.read_schema,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(get_current_user)],  # <-- Exige Auth
    )

    # PUT protégé
    self.router.add_api_route(
        "/{id}",
        self.update,
        methods=["PUT"],
        response_model=self.read_schema,
        dependencies=[Depends(get_current_user)],  # <-- Exige Auth
    )

    # DELETE protégé
    self.router.add_api_route(
        "/{id}",
        self.destroy,
        methods=["DELETE"],
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Depends(get_current_user)],  # <-- Exige Auth
    )
