from sqlmodel import SQLModel, create_engine, Session


database_file = 'data.db'
database_connection_string = f"sqlite:///{database_file}"
connect_args = {
    "check_same_thread": False
}
engine = create_engine(
    database_connection_string,
    echo=True,
    connect_args=connect_args
)


def conn():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
