#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import random
import smtplib
import hashlib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .. import app

def pwgen(length=15, hex=False):
    """
    Генератор пароля
    """
    keylist='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if hex:
        keylist='0123456789ABCDEF'
    password=[]

    while len(password) < length:
        a_char = random.choice(keylist)
        password.append(a_char)
    return ''.join(password)

def get_hash_password(password, salt = None):
    """
    Получить хеш пароля SHA-512
    """
    if salt == None:
        salt = uuid.uuid4().hex
    text = password.encode('utf-8') + salt.encode('utf-8')
    h = hashlib.sha512()
    h.update(text)
    return str(h.hexdigest())
