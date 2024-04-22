from sqlalchemy import URL, create_engine
from .db_tables import Base


DATABASE_URL = URL.create(
    drivername="sqlite",
    database="./db/synoptic.db",
)


engine = create_engine(
    url=DATABASE_URL,
    echo=True
)


def create_db():
    Base.metadata.create_all(
        bind=engine
    )
