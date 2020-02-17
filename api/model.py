import os
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


base     = declarative_base()
user     = 'root'
password = os.environ.get("MYSQL_ROOT_PASSWORD")
host     = os.environ.get("MYSQL_HOST")
dbname   = 'weather'
uri      = 'mysql://%s:%s@%s/%s?charset=utf8' % (user, password, host, dbname)
engine   = create_engine(uri, echo=True)


class Area(base):
    __tablename__ = 'areas'

    id           = Column(Integer, primary_key=True)
    area_id      = Column(String(16))
    area_name    = Column(String(16))
    area_api_uri = Column(Text)


def list_city_code():
    Session    = sessionmaker(bind=engine)
    session    = Session()
    areas      = session.query(Area).all()
    city_codes = []

    for area in areas:
        city_codes.append(area.area_id)

    return city_codes


def get_city_name(city_code):
    Session = sessionmaker(bind=engine)
    session = Session()
    areas   = session.query(Area).filter(Area.area_id==city_code).all()

    if len(areas) == 0:
        return None
    else:
        return areas[0].area_name