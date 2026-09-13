from src.core.crud import CRUDRouter, SQLModelCRUD
from src.documentation.models import (
    Category,
    CategoryCreate,
    CategoryRead,
    CategoryUpdate
)


category_service = SQLModelCRUD(model=Category)

category_router = CRUDRouter(
    crud_service=category_service,
    create_schema=CategoryCreate,
    read_schema=CategoryRead,
    update_schema=CategoryUpdate,
    prefix="/categories",
    tags=["Categories"]
)
