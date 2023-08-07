"""
Models for the base app.
"""

from datetime import datetime
import pymysql

from sqlalchemy import Boolean, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapped_column


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


class ModelBase:
    """
    Model base.
    """

    id = mapped_column(Integer, primary_key=True, index=True, sort_order=-10)
    create_time = mapped_column(DateTime, default=datetime.now, index=True, sort_order=-9,
                                comment="创建时间")
    modified_time = mapped_column(DateTime, onupdate=datetime.now, index=True, sort_order=-8,
                                  comment="修改时间")
    is_delete = mapped_column(Boolean, default=False, sort_order=-7, comment="是否删除")
