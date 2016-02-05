# -*- coding: utf-8 -*-
# @Date    : 2016-02-03 下午11:16
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from flask import request, current_app, render_template, flash, redirect, url_for
from flask.ext.menu import register_menu

from ..ext import db
from .models import User
from .forms import LoginForm, RegisterForm
from .utils import UserManager

auth = UserManager('auth',
                   __name__,
                   url_prefix='/auth',
                   template_folder='templates',
                   static_url_path='/static/core',
                   static_folder='static')

if not current_app.config.get('AUTH_PROFILE_VIEW'):
    @auth.route('/profile/')
    @auth.login_required
    @register_menu(auth, '.auth.profile', u'注销', order=1)
    def profile():
        return render_template('auth/profile.html')


@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            auth.login(user)
            flash(u'欢迎您, {user} '.format(user=user.username), 'success')
            redirect_name = current_app.config.get('AUTH_PROFILE_VIEW', 'auth.profile')
            return redirect(url_for(redirect_name))
        flash(u'无效用户名或密码', 'error')
    return redirect(request.referrer or url_for(auth._login_manager.login_view))


@auth.route('/logout')
@auth.login_required
@register_menu(auth, '.auth.logout', u'注销', order=2)
def logout():
    auth.logout()
    return redirect(request.referrer or url_for(auth._login_manager.login_view))


@auth.route('/register', methods=['GET', 'POST'])
@register_menu(auth, '.auth.register', u'注册', order=0)
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            pw_hash=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        auth.login(user)

        flash(u'感谢您的注册', 'success')

        redirect_name = current_app.config.get('AUTH_PROFILE_VIEW', 'auth.profile')
        return redirect(url_for(redirect_name))
    return render_template('auth/register.html', form=form)
