from src.core.crud import CRUDRouter, SQLModelCRUD
from src.documentation.models import (
    Post,
    PostCreate,
    PostRead,
    PostUpdate
)


post_service = SQLModelCRUD(model=Post)

post_router = CRUDRouter(
    crud_service=post_service,
    create_schema=PostCreate,
    read_schema=PostRead,
    update_schema=PostUpdate,
    prefix="/posts",
    tags=["Posts"]
)
