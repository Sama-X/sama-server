"""
Models for the base app.
"""

import pymysql

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from base import config

pymysql.install_as_MySQLdb()

settings = config.get_settings()

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Get the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
