#!/usr/bin/env python3.4
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import config
import logging

from flask import Flask
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(config.CONFIG)

# Логирование
handler = RotatingFileHandler(
    app.config['LOG_FILE'],
    maxBytes=app.config['LOG_FILE_SIZE']*1024*1024,
    backupCount=1
)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(app.config['LONG_LOG_FORMAT'])
handler.setFormatter(formatter)
app.logger.setLevel(logging.INFO) # root level's
app.logger.addHandler(handler)

# celery
from celery import Celery

celery = Celery(app.name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND'],
    include=['helpdesk.tasks'])
celery.conf.update(app.config)

#from .bp_acl import bp_acl as acl_blueprint
#app.register_blueprint(acl_blueprint, url_prefix='/acl')

#from .bp_user import bp_user as user_blueprint
#app.register_blueprint(user_blueprint, url_prefix='/user')

from . import views
