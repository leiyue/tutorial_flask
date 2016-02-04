# -*- coding: utf-8 -*-
# @Date    : 2016-02-03 下午4:45
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from flask import request
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class EmailFormMixin(object):

    email = StringField(u'邮件地址', validators=[
        DataRequired(message=u'请填写邮件地址'),
        Email(message=u'邮件地址无效')
    ])


class PasswordFormMixin(object):

    password = PasswordField(u'密码', validators=[
        DataRequired(message=u'请填写密码')
    ])


class PasswordConfirmFormMixin(object):

    password_confirm = PasswordField(u'重复密码', validators=[
        EqualTo('password', message=u'两次密码不相符')
    ])


class LoginForm(Form, EmailFormMixin, PasswordField):

    remember = BooleanField(u'记住我', default=True)
    next = HiddenField()
    submit = SubmitField(u'登录')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        if request.method == 'GET':
            self.next.data = request.args.get('next', None)


class ForgotPasswordForm(Form, EmailFormMixin):

    submit = SubmitField(u'忘记密码')

    def to_dict(self):
        return dict(email=self.email.data)


class RegisterForm(Form, EmailFormMixin, PasswordFormMixin, PasswordConfirmFormMixin):

    username = StringField(u'用户名', validators=[
        DataRequired(message=u'请填写用户名')
    ])
    submit = SubmitField(u'注册')

    def to_dict(self):
        return dict(email=self.email.data, password=self.password.data)


class ResetPasswordForm(Form, EmailFormMixin, PasswordFormMixin, PasswordConfirmFormMixin):

    token = HiddenField(validators=[DataRequired()])
    submit = SubmitField(u'重置密码')

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

        if request.method == 'GET':
            self.token.data = request.args.get('token', None)
            self.email.data = request.args.get('email', None)

    def to_dict(self):
        return dict(token=self.token.data, email=self.email.data, password=self.password.data)
