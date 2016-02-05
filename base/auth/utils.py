# -*- coding: utf-8 -*-
# @Date    : 2016-02-03 下午11:19
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from flask import Blueprint
from flask.ext.login import LoginManager, login_required, logout_user, login_user, current_user
from flask.ext.principal import Principal, identity_loaded, identity_changed, AnonymousIdentity, Identity, UserNeed, \
    RoleNeed

from ..ext import db
from .models import User


class UserManager(Blueprint):
    def __init__(self, *args, **kwargs):
        self._login_manager = None
        self._principal = None
        self.app = None
        super(UserManager, self).__init__(*args, **kwargs)

    def register(self, app, *args, **kwargs):

        if not self._login_manager or self.app != app:
            self._login_manager = LoginManager()
            self._login_manager.user_callback = self.user_loader
            self._login_manager.init_app(app)
            self._login_manager.login_view = app.config.get('AUTH_LOGIN_VIEW', 'core.index')
            self._login_manager.login_message = u'您需要登录授权才能访问'

        self.app = app

        if not self._principal:
            self._principal = Principal(app)
            identity_loaded.connect(self.identity_loaded)

        super(UserManager, self).register(app, *args, **kwargs)

    @staticmethod
    def user_loader(pk):
        return User.query.options(db.joinedload(User.roles)).get(pk)

    @staticmethod
    def login_required(fn):
        return login_required(fn)

    def logout(self):
        identity_changed.send(self.app, identity=AnonymousIdentity())
        return logout_user()

    def login(self, user):
        identity_changed.send(self.app, identity=Identity(user.id))
        return login_user(user)

    @staticmethod
    def identity_loaded(sender, identity):
        identity.user = current_user

        if current_user.is_authenticated:
            identity.provides.add(UserNeed(current_user.id))

            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
