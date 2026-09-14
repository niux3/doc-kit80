from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. Imports SQLModel, Settings et Modèles
from sqlmodel import SQLModel
from src.core.settings import settings  # Ajusté selon l'arborescence

from src.documentation.models import Language, Category, Post  # noqa: F401
from src.registration.models import User  # noqa: F401

# 2. Initialisation de la configuration Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Métadonnées et URL dynamique
target_metadata = SQLModel.metadata
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """Mode offline : génère le SQL sans se connecter à la BDD."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Mode online : exécute les migrations directement sur la BDD."""

    # Active render_as_batch uniquement si on est sur SQLite
    is_sqlite = settings.DATABASE_URL.startswith("sqlite")

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=is_sqlite,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
