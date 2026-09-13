from src.documentation.routes.language import language_router
from src.documentation.routes.category import category_router
from src.documentation.routes.post import post_router


documentation_routers = [
    language_router,
    category_router,
    post_router
]
