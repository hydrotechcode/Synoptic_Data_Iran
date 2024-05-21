from sqlalchemy import URL, create_engine
from db.db_tables import Base

from sqlalchemy.orm import sessionmaker
from db.db_tables import SynopticData, SynopticGeoInfo

DATABASE_URL = URL.create(
    drivername="sqlite",
    database="db/synoptic.db",
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
    