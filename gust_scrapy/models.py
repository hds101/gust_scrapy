from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import gust_scrapy.settings


Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**gust_scrapy.settings.DATABASE))

def create_table(engine):
    Base.metadata.create_all(engine)


class GustCompany(Base):
    __tablename__ = "gust_companies"

    id = Column(Integer, primary_key=True)
    gust_users = relationship("GustUser", back_populates="gust_company")

    url = Column('url', String)
    name = Column('name', String, nullable=True)
    slogan = Column('slogan', Text, nullable=True)
    overview = Column('overview', Text, nullable=True)
    # Data
    industry = Column('industry', String, nullable=True)
    location = Column('location', String, nullable=True)
    currency = Column('currency', String, nullable=True)
    founded = Column('founded', String, nullable=True)
    employees = Column('employees', Integer, nullable=True)
    stage = Column('stage', String, nullable=True)
    website = Column('website', String, nullable=True)
    incorporation_type = Column('incorporation_type', String, nullable=True)


class GustUser(Base):
    __tablename__ = "gust_users"

    id = Column(Integer, primary_key=True)
    gust_company_id = Column(Integer, ForeignKey('gust_companies.id'))
    gust_company = relationship("GustCompany", back_populates="gust_users")

    tag = Column('tag', String)
    url = Column('url', String)
    name = Column('name', String, nullable=True)
    location = Column('location', String, nullable=True)
    role = Column('role', Text, nullable=True)
    biography = Column('biography', Text, nullable=True)
    website = Column('website', String, nullable=True)
    social_linkedin = Column('social_linkedin', String, nullable=True)
    social_twitter = Column('social_twitter', String, nullable=True)
    social_facebook = Column('social_facebook', String, nullable=True)
