#!/usr/bin/env python3.4
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from functools import wraps
from flask import (
    Flask,
    Markup,
    session,
    request,
    g,
    url_for,
    escape,
    redirect,
    render_template,
    Response,
    jsonify,
    abort,
    send_file
)

import io
import os
import json
import email
import poplib

# Crypt and hash
import uuid
import hashlib
import datetime

from sqlalchemy import and_, or_
# RemiZOffAlex
from . import app, lib, models, forms


@app.route('/')
def index():
    """Главная страница"""
    pagedata = {'title': ' - '.format(app.config['TITLE'])}
    body = render_template('index.html', pagedata=pagedata)
    return body


@app.route('/certificates', defaults={'page': 1})
@app.route('/certificates/<int:page>')
def certificates(page):
    """Список сертификатов"""
    pagedata = {'title': 'Список сертификатов - '.format(app.config['TITLE'])}
    pagedata['certificates'] = models.db_session.query(
        models.Certificate
    )
    pagedata['pagination'] = lib.Pagination(
        page,
        10,
        pagedata['certificates'].count()
    )
    pagedata['pagination'].url = '/certificates'
    pagedata['certificates'] = lib.getpage(pagedata['certificates'], page)
    pagedata['certificates'] = pagedata['certificates'].all()
    body = render_template('certificates.html', pagedata=pagedata)
    return body


@app.route('/generateca', methods=['GET', 'POST'])
def generateca():
    pagedata = {'title': app.config['TITLE']}
    pagedata['form'] = forms.NewCertificateForm(request.form)
    if request.method == 'POST':
        from OpenSSL import crypto, SSL
        # Создать пару ключей
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        # Создать самоподписанный сертификат
        cert = crypto.X509()
        if pagedata['form'].C.data:
            cert.get_subject().C = pagedata['form'].C.data
        if pagedata['form'].ST.data:
            cert.get_subject().ST = pagedata['form'].ST.data
        if pagedata['form'].L.data:
            cert.get_subject().L = pagedata['form'].L.data
        if pagedata['form'].O.data:
            cert.get_subject().O = pagedata['form'].O.data
        if pagedata['form'].OU.data:
            cert.get_subject().OU = pagedata['form'].OU.data
        if pagedata['form'].CN.data:
            cert.get_subject().CN = pagedata['form'].CN.data
        cert.set_serial_number(1)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60) # 10 лет
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')
        cert.sign(k, 'sha256')
        cert.sign(k, 'sha512')
        pagedata['cert'] = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8')
        pagedata['key'] = crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode('utf-8')
        body = render_template('certificate_view.html', pagedata=pagedata)
        return body
    body = render_template('generateca.html', pagedata=pagedata)
    return body


@app.route('/menu')
def menu():
    """Меню"""
    pagedata = {'title': app.config['TITLE']}
    body = render_template('menu.html', pagedata=pagedata)
    return body


# noinspection PyUnusedLocal
@app.errorhandler(404)
def error_missing(exception):
    pagedata = {}
    pagedata['title'] = app.config['TITLE']
    error_message = "Не судьба..."
    return render_template("error.html", error_code=404, error_message=error_message, pagedata=pagedata), 404


# noinspection PyUnusedLocal
@app.errorhandler(403)
def error_unauthorized(exception):
    pagedata = {}
    pagedata['title'] = app.config['TITLE']
    error_message = "У Вас нет достаточных прав для доступа к данному ресурсу"
    return render_template("error.html", error_code=403, error_message=error_message, pagedata=pagedata), 403

# noinspection PyUnusedLocal
@app.errorhandler(500)
def error_crash(exception):
    pagedata = {}
    pagedata['title'] = app.config['TITLE']
    error_message = "Вот незадача..."
    return render_template("error.html", error_code=500, error_message=error_message, pagedata=pagedata), 500
