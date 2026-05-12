from sqlmodel import create_engine, SQLModel, Session
from config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    echo = False, 
    connect_args={
        "check_same_thread" : False
    })


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_sessions():
    with Session(engine) as session:
        yield session