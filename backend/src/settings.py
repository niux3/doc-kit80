"""
Configuration centralisée de l'application.
Utilise pydantic-settings pour la validation et python-dotenv pour le chargement.
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Configuration de l'application chargée depuis .env"""

    model_config = SettingsConfigDict(
        env_file=".env",           # Charge le fichier .env
        env_file_encoding="utf-8",
        case_sensitive=False,      # Insensible à la casse
        extra="ignore"             # Ignore les variables non définies
    )

    # ============ APPLICATION ============
    APP_NAME: str = "doc-kit80"
    APP_VERSION: str = "0.0.1"
    APP_ENV: str = "development"  # development, staging, production
    DEBUG: bool = True

    # ============ SERVEUR ============
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ============ BASE DE DONNÉES ============
    DB_FILE: str = "data.db"
    DATABASE_URL: Optional[str] = None  # Sera construit automatiquement

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: Optional[str], info) -> str:
        """Construit l'URL de la BD si pas explicitement fournie"""
        if isinstance(v, str) and v:
            return v
        db_file = info.data.get("DB_FILE", "data.db")
        return f"sqlite:///{db_file}"

    # ============ CORS / SÉCURITÉ ============
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",    # Vite dev
        "http://localhost:3000",    # Alternative
    ]

    # Secret pour JWT ou sessions (à générer : openssl rand -hex 32)
    SECRET_KEY: str = "change-me-in-production-please!"

    # ============ DOSSIERS ============
    BASE_DIR: Path = Path(__file__).resolve().parent.parent  # backend/
    DATA_DIR: Path = Path("data")  # Pour CSV, exports, etc.
    LOGS_DIR: Path = Path("logs")

    # ============ LOGGING ============
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


settings = Settings()
