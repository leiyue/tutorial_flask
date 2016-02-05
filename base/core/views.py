# -*- coding: utf-8 -*-
# @Date    : 2016-01-31 13:15
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from flask import Blueprint, render_template
from flask_menu import register_menu

from base.auth.forms import LoginForm

core = Blueprint('urls',
                 __name__,
                 template_folder='templates',
                 static_url_path='/static/core',
                 static_folder='static')


@core.route('/')
@register_menu(core, '.main.home', u'首页', order=0)
def index():
    form = LoginForm()
    return render_template('core/index.html',
                           title=u'首页',
                           form=form)
