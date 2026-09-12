from src.core.crud import CRUDRouter, SQLModelCRUD
from src.documentation.models import (
    Language,
    LanguageCreate,
    LanguageRead,
    LanguageUpdate
)


language_service = SQLModelCRUD(model=Language)

language_router = CRUDRouter(
    crud_service=language_service,
    create_schema=LanguageCreate,
    read_schema=LanguageRead,
    update_schema=LanguageUpdate,
    prefix="/languages",
    tags=["Languages"]
)
