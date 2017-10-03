#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import datetime
from sqlalchemy import Table, Column, Boolean, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from . import Base


class Certificate(Base):
    __tablename__ = "certificate"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('certificate.id'))
    name = Column(String)
    description = Column(String)
    created = Column(DateTime) # Дата создания/регистрации
    disabled = Column(Boolean, default=False)

    # Связи
    #contacts = relationship("Contact", primaryjoin="User.id==Contact.user_id")
    parent = relationship(
        "Certificate",
        primaryjoin="Certificate.parent_id==Certificate.id",
        uselist=False
    )
    private = relationship(
        "Private",
        primaryjoin="Certificate.id==Private.certificate_id",
        uselist=False
    )
    public = relationship(
        "Public",
        primaryjoin="Certificate.id==Public.certificate_id",
        uselist=False
    )
    csr = relationship(
        "CSR",
        primaryjoin="Certificate.id==CSR.certificate_id",
        uselist=False
    )

    def __init__(self, name):
        self.name = name
        self.created = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Сертификат %r>' % (self.name)


class Private(Base):
    __tablename__ = "private"

    id = Column(Integer, primary_key=True)
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    body = Column(String)
    created = Column(DateTime) # Дата создания/регистрации

    # Связи
    #contacts = relationship("Contact", primaryjoin="User.id==Contact.user_id")
    certificate = relationship(
        "Certificate",
        primaryjoin="Private.certificate_id==Certificate.id",
        uselist=False
    )

    def __init__(self, certificate):
        self.certificate_id = certificate.id
        self.created = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Закрытый ключ сертификата {}>'.format(self.certificate.name)


class Public(Base):
    __tablename__ = "public"

    id = Column(Integer, primary_key=True)
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    body = Column(String)
    created = Column(DateTime) # Дата создания/регистрации

    # Связи
    #contacts = relationship("Contact", primaryjoin="User.id==Contact.user_id")
    certificate = relationship(
        "Certificate",
        primaryjoin="Public.certificate_id==Certificate.id",
        uselist=False
    )

    def __init__(self, certificate):
        self.certificate_id = certificate.id
        self.created = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Публичный ключ сертификата {}>'.format(self.name)


class CSR(Base):
    __tablename__ = "csr"

    id = Column(Integer, primary_key=True)
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    body = Column(String)
    created = Column(DateTime) # Дата создания/регистрации

    # Связи
    #contacts = relationship("Contact", primaryjoin="User.id==Contact.user_id")
    certificate = relationship(
        "Certificate",
        primaryjoin="CSR.certificate_id==Certificate.id",
        uselist=False
    )

    def __init__(self, certificate):
        self.certificate_id = certificate.id
        self.created = datetime.datetime.utcnow()

    def __repr__(self):
        return '<CSR {}>'.format(self.name)


class Field(Base):
    __tablename__ = "field"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fieldtype = Column(String)
    description = Column(String)
    required = Column(Boolean, default=False)

    # Связи
    #contacts = relationship("Contact", primaryjoin="User.id==Contact.user_id")
    # certificate = relationship("Certificate", primaryjoin="CSR.certificate_id==Certificate.id")

    def __init__(self, name, fieldtype):
        self.name = name

    def __repr__(self):
        return '<Field {}>'.format(self.name)


class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True)
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    field_id = Column(Integer, ForeignKey('field.id'))
    value = Column(String)

    # Связи
    #contacts = relationship("Contact", primaryjoin="User.id==Contact.user_id")
    certificate = relationship(
        "Certificate",
        primaryjoin="Subject.certificate_id==Certificate.id",
        uselist=False
    )
    field = relationship(
        "Field",
        primaryjoin="Subject.field_id==Field.id",
        uselist=False
    )

    def __init__(self, certificate, field):
        self.certificate_id = certificate.id
        self.field_id = field.id

    def __repr__(self):
        return '<Subject {}>'.format(self.name)
