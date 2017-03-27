#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from .. import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
if not database_exists(engine.url):
    create_database(engine.url)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

#from .user import User

Base.metadata.create_all(engine)

__all__ = [
    'db_session',
    'User',
    'ObjectPermission', 'UserPermission'
]
