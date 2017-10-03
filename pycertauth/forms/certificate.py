#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from wtforms import Form, TextField, SelectField

class NewCertificateForm(Form):
    C = SelectField('Страна (C)', choices=[('RU', 'RU'), ('EN', 'EN')])
    ST = TextField('Край, область (ST)', render_kw={'placeholder': 'Москва'})
    L = TextField('Город (L)', render_kw={'placeholder': 'Москва'})
    O = TextField('Название организации (O)')
    OU = TextField('Отдел (OU)', render_kw={'placeholder': 'IT'})
    CN = TextField('Имя домена (CN)', render_kw={'placeholder': 'remizoffalex.ru'})
    emailAddress = TextField('Адрес электронной почты (emailAddress)')
