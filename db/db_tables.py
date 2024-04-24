from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Float, String, Date


Base = declarative_base()


class SynopticData(Base):

    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    st_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    temperature_max = Column(Float)
    temperature_mean = Column(Float)
    temperature_min = Column(Float)
    precipitation = Column(Float)

    synoptic_geoinfo_id = Column(Integer, ForeignKey("geoinfo.id"))

    synoptic_geoinfo = relationship(
        "SynopticGeoInfo",
        back_populates="synoptic_data"
    )

    def __repr__(self):
        return f"<Station(ID='{self.st_id}', Date='{self.date}')>"


class SynopticGeoInfo(Base):

    __tablename__ = 'geoinfo'

    id = Column(Integer, primary_key=True)
    st_id = Column(Integer, unique=True, nullable=False)
    st_name = Column(String, nullable=False)
    st_latitude = Column(Float, nullable=False)
    st_longitude = Column(Float, nullable=False)
    st_altitude = Column(Float, nullable=False)

    synoptic_data = relationship("SynopticData")

    def __repr__(self):
        return f"<Station(ID='{self.st_id}', Name={self.st_name}')>"
