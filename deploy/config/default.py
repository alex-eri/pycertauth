#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import os
import sys


DEBUG = True
SQLDEBUG = False
DIR_BASE = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])
DIR_DATA = DIR_BASE + '/data'
DIR_FILES = DIR_DATA + '/files'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DIR_DATA + '/db.sqlite3'
SECRET_KEY = 'here_secret_key'

SESSION_COOKIE_NAME = 'pycertauth'
SESSION_TYPE = 'filesystem'

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

TITLE = "Центр сертификации"

# Логирование
LOG_FILE = DIR_BASE + '/logs/pycertauth.log'
LONG_LOG_FORMAT = '%(asctime)s - [%(name)s.%(levelname)s] [%(threadName)s, %(module)s.%(funcName)s@%(lineno)d] %(message)s'
LOG_FILE_SIZE = 128

# Количество выводимых элементов на странице
ITEMS_ON_PAGE = 100
