#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from flask import render_template, request, redirect, escape
from OpenSSL import crypto, SSL

from . import bp_certificate, forms
from .. import app, lib, models

@bp_certificate.route('/<int:id>')
def certificate_id(id):
    pagedata = {'title': 'Сертификат - ' + app.config['TITLE']}
    pagedata['certificate'] = models.db_session.query(
        models.Certificate
    ).filter(
        models.Certificate.id==id
    ).first()
    body = render_template('certificate.html', pagedata=pagedata)
    return body


@bp_certificate.route('/<int:id>/csr', methods=['GET', 'POST'])
def certificate_csr(id):
    """Запрос на получение сертификата"""
    pagedata = {'title': 'Запрос на получение сертификата - {}'.format(app.config['TITLE'])}
    pagedata['certificate'] = models.db_session.query(
        models.Certificate
    ).filter(
        models.Certificate.id==id
    ).first()
    if pagedata['certificate'] is None:
        abort(404)
    if pagedata['certificate'].csr is None:
        pagedata['form'] = forms.CSRCertificateForm(request.form)
    else:
        pagedata['form'] = forms.CSRCertificateForm(
            request.form,
            data={
                'body': pagedata['certificate'].csr.body
            }
        )
    if request.method == 'POST':
        if pagedata['form'].validate():
            if pagedata['certificate'].csr is None:
                newcsr = models.CSR(pagedata['certificate'])
                models.db_session.add(newcsr)
                models.db_session.commit()
            pagedata['certificate'].csr.body = pagedata['form'].body.data
            models.db_session.commit()
    body = render_template('certificate_csr.html', pagedata=pagedata)
    return body


@bp_certificate.route('/<int:id>/csr/delete', methods=['GET', 'POST'])
def certificate_csr_delete(id):
    """Удаление CSR запроса"""
    pagedata = {'title': 'Удаление CSR запроса - {}'.format(app.config['TITLE'])}
    pagedata['certificate'] = models.db_session.query(
        models.Certificate
    ).filter(
        models.Certificate.id==id
    ).first()
    if pagedata['certificate'] is None:
        abort(404)
    if pagedata['certificate'].csr is None:
        abort(404)
    pagedata['form'] = forms.DeleteCSRCertificateForm(request.form)
    if request.method == 'POST':
        if pagedata['form'].validate():
            models.db_session.delete(pagedata['certificate'].csr)
            models.db_session.commit()
            return redirect('/certificate/{}'.format(id), code=302)
    body = render_template('certificate_csr_delete.html', pagedata=pagedata)
    return body


@bp_certificate.route('/<int:id>/edit', methods=['GET', 'POST'])
def certificate_edit(id):
    """Редактирование сертификата"""
    pagedata = {'title': 'Редактирование сертификата - ' + app.config['TITLE']}
    pagedata['certificate'] = models.db_session.query(
        models.Certificate
    ).filter(
        models.Certificate.id==id
    ).first()
    if pagedata['certificate'] is None:
        abort(404)
    pagedata['form'] = forms.EditCertificateForm(
        request.form,
        data={
            'name': pagedata['certificate'].name,
            'description': pagedata['certificate'].description
        }
    )
    if request.method == 'POST':
        if pagedata['form'].validate():
            pagedata['certificate'].name = pagedata['form'].name.data
            pagedata['certificate'].description = pagedata['form'].description.data
            models.db_session.commit()
    body = render_template('certificate_edit.html', pagedata=pagedata)
    return body


@bp_certificate.route('/<int:id>/generate', methods=['GET', 'POST'])
def certificate_generate(id):
    """Генерирование сертификата"""
    pagedata = {'title': 'Генерирование сертификата - ' + app.config['TITLE']}
    pagedata['certificate'] = models.db_session.query(
        models.Certificate
    ).filter(
        models.Certificate.id==id
    ).first()
    if pagedata['certificate'] is None:
        abort(404)
    pagedata['form'] = forms.GenerateCertificateForm(
        request.form,
        data={
            'name': pagedata['certificate'].name,
            'description': pagedata['certificate'].description
        }
    )
    if request.method == 'POST':
        if pagedata['form'].validate():
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
            if pagedata['certificate'].public is None:
                newpublic = models.Public(pagedata['certificate'])
                models.db_session.add(newpublic)
                models.db_session.commit()
            pagedata['certificate'].public.body = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8')
            models.db_session.commit()
            if pagedata['certificate'].private is None:
                newprivate = models.Private(pagedata['certificate'])
                models.db_session.add(newprivate)
                models.db_session.commit()
            pagedata['certificate'].private.body = crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode('utf-8')
            models.db_session.commit()
            return redirect('/certificate/{}'.format(id), code=302)
    body = render_template('certificate_generate.html', pagedata=pagedata)
    return body


@bp_certificate.route('/<int:id>/private', methods=['GET', 'POST'])
def certificate_private(id):
    """Редактирование закрытого ключа сертификата"""
    pagedata = {'title': 'Редактирование закрытого ключа сертификата - {}'.format(app.config['TITLE'])}
    pagedata['certificate'] = models.db_session.query(
        models.Certificate
    ).filter(
        models.Certificate.id==id
    ).first()
    if pagedata['certificate'] is None:
        abort(404)
    if pagedata['certificate'].private is None:
        pagedata['form'] = forms.PrivateCertificateForm(request.form)
    else:
        pagedata['form'] = forms.PrivateCertificateForm(
            request.form,
            data={
                'body': pagedata['certificate'].private.body
            }
        )
    if request.method == 'POST':
        if pagedata['form'].validate():
            if pagedata['certificate'].private is None:
                newprivate = models.Private(pagedata['certificate'])
                models.db_session.add(newprivate)
                models.db_session.commit()
            pagedata['certificate'].private.body = pagedata['form'].body.data
            models.db_session.commit()
    body = render_template('certificate_private.html', pagedata=pagedata)
    return body


@bp_certificate.route('/<int:id>/private/delete', methods=['GET', 'POST'])
def certificate_private_delete(id):
    """Удаление закрытого ключа сертификата"""
    pagedata = {'title': 'Удаление закрытого ключа сертификата - {}'.format(app.config['TITLE'])}
    pagedata['certificate'] = models.db_session.query(
        models.Certificate
    ).filter(
        models.Certificate.id==id
    ).first()
    if pagedata['certificate'] is None:
        abort(404)
    if pagedata['certificate'].private is None:
        abort(404)
    pagedata['form'] = forms.DeletePrivateCertificateForm(request.form)
    if request.method == 'POST':
        if pagedata['form'].validate():
            models.db_session.delete(pagedata['certificate'].private)
            models.db_session.commit()
            return redirect('/certificate/{}'.format(id), code=302)
    body = render_template('certificate_private_delete.html', pagedata=pagedata)
    return body


@bp_certificate.route('/<int:id>/public', methods=['GET', 'POST'])
def certificate_public(id):
    """Редактирование открытого ключа сертификата"""
    pagedata = {'title': 'Редактирование открытого ключа сертификата - {}'.format(app.config['TITLE'])}
    pagedata['certificate'] = models.db_session.query(
        models.Certificate
    ).filter(
        models.Certificate.id==id
    ).first()
    if pagedata['certificate'] is None:
        abort(404)
    if pagedata['certificate'].public is None:
        pagedata['form'] = forms.PublicCertificateForm(request.form)
    else:
        pagedata['form'] = forms.PublicCertificateForm(
            request.form,
            data={
                'body': pagedata['certificate'].public.body
            }
        )
    if request.method == 'POST':
        if pagedata['form'].validate():
            if pagedata['certificate'].public is None:
                newpublic = models.Public(pagedata['certificate'])
                models.db_session.add(newpublic)
                models.db_session.commit()
            pagedata['certificate'].public.body = pagedata['form'].body.data
            models.db_session.commit()
    body = render_template('certificate_public.html', pagedata=pagedata)
    return body


@bp_certificate.route('/<int:id>/public/delete', methods=['GET', 'POST'])
def certificate_public_delete(id):
    """Удаление открытого ключа сертификата"""
    pagedata = {'title': 'Удаление открытого ключа сертификата - {}'.format(app.config['TITLE'])}
    pagedata['certificate'] = models.db_session.query(
        models.Certificate
    ).filter(
        models.Certificate.id==id
    ).first()
    if pagedata['certificate'] is None:
        abort(404)
    if pagedata['certificate'].public is None:
        abort(404)
    pagedata['form'] = forms.DeletePublicCertificateForm(request.form)
    if request.method == 'POST':
        if pagedata['form'].validate():
            models.db_session.delete(pagedata['certificate'].public)
            models.db_session.commit()
            return redirect('/certificate/{}'.format(id), code=302)
    body = render_template('certificate_public_delete.html', pagedata=pagedata)
    return body


@bp_certificate.route('/add', methods=['GET', 'POST'])
def certificate_add():
    """Добавление нового сертификата"""
    pagedata = {'title': 'Новый сертификат - ' + app.config['TITLE']}
    pagedata['form'] = forms.NewCertificateForm(request.form)
    if request.method == 'POST':
        if pagedata['form'].validate():
            newcertificate = models.Certificate(
                pagedata['form'].name.data,
            )
            newcertificate.description = pagedata['form'].description.data
            models.db_session.add(newcertificate)
            models.db_session.commit()
            return redirect('/certificate/' + str(newcertificate.id), code=302)
    body = render_template('certificate_add.html', pagedata=pagedata)
    return body
