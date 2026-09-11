# src/database.py
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from src.settings import settings


class Database:
    def __init__(self, db_url: str, debug: bool = False) -> None:
        self.connect_args = {"check_same_thread": False}
        self.engine = create_engine(
            db_url,
            echo=debug,
            connect_args=self.connect_args
        )

    def init_db(self) -> None:
        """Crée les tables SQLite au démarrage."""
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        """Dépendance FastAPI pour fournir une session de BDD par requête."""
        with Session(self.engine) as session:
            yield session


# Instanciation unique (Singleton) pour le projet
db = Database(db_url=settings.DATABASE_URL, debug=settings.DEBUG)
