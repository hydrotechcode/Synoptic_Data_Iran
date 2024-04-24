from sqlalchemy import URL, create_engine
from src.db_tables import Base


DATABASE_URL = URL.create(
    drivername="sqlite",
    database="synoptic.db",
)

print(DATABASE_URL)


engine = create_engine(
    url=DATABASE_URL,
    echo=True
)


def create_db():
    Base.metadata.create_all(
        bind=engine
    )
