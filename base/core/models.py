# -*- coding: utf-8 -*-
# @Date    : 2016-02-03 下午12:57
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from datetime import datetime

from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import object_session

from ..ext import db


class UpdateMixin(object):
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)


class BaseMixin(UpdateMixin, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    @property
    def __session__(self):
        return object_session(self)


class Alembic(db.Model):
    __tablename__ = 'alembic_version'
    version_number = db.Column(db.String(32), primary_key=True, nullable=False)


def before_signal(session, *args):
    map(lambda o: hasattr(o, 'before_new') and o.before_new(), session.new)
    map(lambda o: hasattr(o, 'before_delete') and o.before_delete(), session.deleted)

event.listen(db.session.__class__, 'before_flush', before_signal)
