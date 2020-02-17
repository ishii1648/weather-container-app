import os
import requests
import xml.etree.ElementTree as ET
from os.path import join, dirname
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


base = declarative_base()


class Area(base):
    __tablename__ = 'areas'

    id           = Column(Integer, primary_key=True)
    area_id      = Column(String(16))
    area_name    = Column(String(16))
    area_api_uri = Column(Text)


def create_database(user, password, host, dbname):
    uri    = 'mysql://%s:%s@%s' % (user, password, host)
    engine = create_engine(uri, pool_recycle=3600, encoding='utf-8')
    schema = 'CREATE DATABASE IF NOT EXISTS `%s` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;' % dbname

    engine.connect().execute(schema)


def create_tables(engine):
    tables = base.metadata.tables.keys()

    for table in tables:
        schema = 'DROP TABLE IF EXISTS {}'.format(table)
        engine.connect().execute(schema)

    base.metadata.create_all(engine)


def fetch_areas(api_uri):
    area_list     = []
    response      = requests.get(api_uri)
    xml_data      = response.text
    root          = ET.fromstring(xml_data)
    index_weather = 12

    for pref in root[0][index_weather]:
        for pref_child in pref:
            if pref_child.tag == 'city':
                area_list.append(
                    Area(
                        area_id=pref_child.attrib['id'], 
                        area_name=pref_child.attrib['title'], 
                        area_api_uri=pref_child.attrib['source']
                    )
                )

    return area_list


def init_areas_table(engine, area_list):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Area).delete()
    session.add_all(area_list)
    session.commit()


if __name__ == "__main__":
    api_uri   = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'
    area_list = fetch_areas(api_uri)

    user     = 'root'
    password = os.environ.get("MYSQL_ROOT_PASSWORD")
    host     = os.environ.get("MYSQL_HOST")
    dbname   = 'weather'

    create_database(user, password, host, dbname)

    uri    = 'mysql://%s:%s@%s/%s?charset=utf8' % (user, password, host, dbname)
    engine = create_engine(uri, echo=True)

    create_tables(engine)
    init_areas_table(engine, area_list)
