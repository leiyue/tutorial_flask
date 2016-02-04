# -*- coding: utf-8 -*-
# @Date    : 2016-01-31 13:13
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

""" base.core package
"""


def loader_meta(app=None):

    from .views import core
    app.register_blueprint(core)

    from flask_bootstrap import Bootstrap
    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    from flask_menu import Menu
    menu = Menu()
    menu.init_app(app)

    from flask import render_template
    app.errorhandler(404)(lambda e: (render_template('core/404.html'), 404))
    app.errorhandler(500)(lambda e: (render_template('core/404.html'), 500))


loader_meta.priority = 100.0
