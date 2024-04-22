from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKey, Column, Integer, Float, String, Date


Base = declarative_base()


class SynopticGeoInfo(Base):

    __tablename__ = 'geoinfo'

    st_id = Column(Integer, autoincrement=True, primary_key=True)
    st_name = Column(String, nullable=False)
    st_latitude = Column(Float, nullable=False)
    st_longitude = Column(Float, nullable=False)
    st_altitude = Column(Float, nullable=False)

    synoptic_data = relationship('SynopticData', back_populates='synoptic_geoinfo')

    def __repr__(self):
        return f"<Station (ID='{self.st_id}', Name={self.st_name}')>"


class SynopticData(Base):

    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    st_id = Column(Integer)
    date = Column(Date, nullable=False)
    temperature_max = Column(Float)
    temperature_mean = Column(Float)
    temperature_min = Column(Float)
    precipitation = Column(Float)

    synoptic_geoinfo_id = Column(Integer, ForeignKey("geoinfo.st_id"))
    synoptic_geoinfo = relationship("SynopticGeoInfo", back_populates='synoptic_data')

    def __repr__(self):
        return f"<Station(ID='{self.st_id}', Date='{self.date}')>"
