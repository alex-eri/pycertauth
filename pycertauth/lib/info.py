#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from flask import session, request
from .. import models

def get_user():
    """
    Получить текущего пользователя
    """
    result = None
    if 'user_id' in session:
        result = models.db_session.query(models.User).filter(models.User.id==session['user_id']).first()
    return result

def get_ip():
    """Получить IP"""
    result = ''
    if request.headers.getlist("X-Forwarded-For"):
        result = request.headers.get("X-Forwarded-For").split(",")[0]
    else:
        result = request.remote_addr
    print(result)
    return result
