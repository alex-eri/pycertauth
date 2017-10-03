#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from wtforms import Form, TextField, TextAreaField, SelectField


class NewCertificateForm(Form):
    name = TextField('Название')
    description = TextAreaField('Описание')


class EditCertificateForm(Form):
    name = TextField('Название')
    description = TextAreaField('Описание')


class PrivateCertificateForm(Form):
    body = TextAreaField('Закрытый ключ', render_kw={"rows": "10", "style": "font-family: 'Liberation Mono', monospace;"})


class PublicCertificateForm(Form):
    body = TextAreaField('Закрытый ключ', render_kw={"rows": "10", "style": "font-family: 'Liberation Mono', monospace;"})


class CSRCertificateForm(Form):
    body = TextAreaField('Запрос на получение сертификата', render_kw={"rows": "10", "style": "font-family: 'Liberation Mono', monospace;"})


class DeletePrivateCertificateForm(Form):
    """Форма удаление закрытого ключа"""
    pass


class DeleteCSRCertificateForm(Form):
    """Форма удаление CSR запроса"""
    pass


class DeletePublicCertificateForm(Form):
    """Форма удаление открытого ключа"""
    pass


class GenerateCertificateForm(Form):
    C = SelectField('Страна (C)', choices=[('RU', 'RU'), ('EN', 'EN')])
    ST = TextField('Край, область (ST)', render_kw={'placeholder': 'Москва'})
    L = TextField('Город (L)', render_kw={'placeholder': 'Москва'})
    O = TextField('Название организации (O)')
    OU = TextField('Отдел (OU)', render_kw={'placeholder': 'IT'})
    CN = TextField('Имя домена (CN)', render_kw={'placeholder': 'remizoffalex.ru'})
    emailAddress = TextField('Адрес электронной почты (emailAddress)')
