"""
Application Factory pour FastAPI.
Architecture modulaire avec séparation des responsabilités.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.core.settings import settings
from src.core.database import db

# --- models ---
from src.documentation.models import Category, Language, Post
from src.registration.models import User

# --- routes ---
from src.documentation.routes import language_router


def _setup_middlewares(app: FastAPI) -> None:
    """Configure tous les middlewares"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _setup_basic_routes(app: FastAPI) -> None:
    """Routes static"""
    @app.get("/")
    async def root():
        """Page d'accueil de l'API"""
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs" if settings.DEBUG else "Non disponible en production",
            "endpoints": {
                "language": "/api/language",
            }
        }

    @app.get("/api/health")
    async def health_check():
        """Vérification de la santé de l'API"""
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
            "database": settings.DB_NAME,
        }


def _setup_routers(app: FastAPI) -> None:
    """Enregistre tous les routers métier"""
    app.include_router(language_router.router, prefix="/api/v1")


def _setup_exception_handlers(app: FastAPI) -> None:
    """Configure les gestionnaires d'erreurs"""

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content={"error": "Données invalides", "detail": str(exc)}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Erreur interne",
                "detail": str(exc) if settings.DEBUG else "Une erreur est survenue"
            }
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cycle de vie de l'application"""
    # Startup
    db.init_db()

    # Logging des APIs configurées
    # apis = {
    #     "RocketReach": settings.ROCKETREACH_API_KEY,
    #     "ContactOut": settings.CONTACTOUT_API_KEY,
    #     "SendGrid": settings.SENDGRID_API_KEY,
    # }
    # for api_name, api_key in apis.items():
    #     if api_key:
    #         print(f"✅ API {api_name} configurée")
    #
    yield
    print("👋 Arrêt propre")


def create_app() -> FastAPI:
    """
    Application Factory.
    Crée et configure l'application FastAPI.
    """

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs" if settings.DEBUG else None,
    )

    _setup_middlewares(app)
    _setup_routers(app)
    _setup_basic_routes(app)
    _setup_exception_handlers(app)

    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} - {settings.APP_ENV}")

    return app


app = create_app()
