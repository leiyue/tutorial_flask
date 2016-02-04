# -*- coding: utf-8 -*-
# @Date    : 2016-02-03 下午11:16
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from flask import request, current_app, render_template, flash, redirect, url_for

from ..ext import db
from .models import User
from .forms import LoginForm, RegisterForm
from .utils import UserManager

auth = UserManager('auth', url_prefix='/auth', template_folder='templates')

if not current_app.config.get('AUTH_PROFILE_VIEW'):

    @auth.route('/profile/')
    @auth.login_required
    def profile():
        return render_template('auth/profile.html')


@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            auth.login(user)
            flash(u'欢迎您, {user} '.format(user=user.username), 'success')
            redirect_name = current_app.config.get('AUTH_PROFILE_VIEW', 'auth.profile')
            return redirect(url_for(redirect_name))
        flash(u'无效用户名或密码', 'error')
    return redirect(request.referrer or url_for(auth._login_manager.login_view))


@auth.route('/logout')
@auth.login_required
def logout():
    auth.logout()
    return redirect(request.referrer or url_for(auth._login_manager.login_view))

@auth.route('/register', methods=['GET', 'POST'])
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