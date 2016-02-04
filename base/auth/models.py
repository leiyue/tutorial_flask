# -*- coding: utf-8 -*-
# @Date    : 2016-02-03 下午2:50
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

import string
import random
from datetime import datetime

from flask.ext.login import UserMixin
from flask.ext.principal import Permission, RoleNeed
from flask.ext.sqlalchemy import _BoundDeclarativeMeta
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from ..core.models import BaseMixin
from ..ext import db

userroles = db.Table(
    'auth_userroles',
    db.Column('user_id', db.Integer, db.ForeignKey('auth_user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('auth_role.id'))
)


class Role(db.Model, BaseMixin):
    """ User Role
    """

    __tablename__ = 'auth_role'

    name = db.Column(db.String(19), unique=True, nullable=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class UserMixinMeta(_BoundDeclarativeMeta):
    def __new__(mcs, name, bases, params):
        from flask import current_app
        from importlib import import_module

        if current_app and current_app.config.get('AUTH_USER_MIXINS'):
            for mixin in current_app.config.get('AUTH_USER_MIXINS'):
                mod, cls = mixin.rsplit('.', 1)
                mod = import_module(mod)
                cls = getattr(mod, cls)
                bases = bases + (cls,)

        return super(UserMixinMeta, mcs).__new__(mcs, name, bases, params)


class User(db.Model, UserMixin, BaseMixin):
    __tablename__ = 'auth_user'
    __metaclass__ = UserMixinMeta

    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=False)
    _pw_hash = db.Column(db.String(255), nullable=False)

    @declared_attr
    def roles(self):
        assert self
        return db.relationship('Role', secondary=userroles, backref='users')

    @hybrid_property
    def pw_hash(self):
        return self._pw_hash

    @pw_hash.setter
    def pw_hash(self, raw_password):
        self._pw_hash = generate_password_hash(raw_password)

    @staticmethod
    def permission(role):
        perm = Permission(RoleNeed(role))
        return perm.can()

    def generate_password(self):
        self.pw_hash = ''.join(random.choice(string.letters + string.digits) for i in range(8))

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_active(self):
        return self.active

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Key(db.Model, BaseMixin):
    __tablename__ = 'auth_key'
    __table_agrs__ = db.UniqueConstraint('service_alias', 'service_id')

    service_alias = db.Column(db.String)
    service_id = db.Column(db.String)

    access_token = db.Column(db.String)
    secret = db.Column(db.String)
    expires = db.Column(db.DateTime)
    refresh_token = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    user = db.relationship('User', backref=db.backref('key', lazy='dynamic'))

    def __unicode__(self):
        return self.service_alias

    def __repr__(self):
        return '<Key {}>'.format(self.service_alias)

    def is_expired(self):
        return self.expires and self.expires < datetime.now()
