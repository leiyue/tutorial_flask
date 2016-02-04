# -*- coding: utf-8 -*-
# @Date    : 2016-02-01 0:07
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

""" base.auth package
"""


def loader_meta(app):

    from .views import auth
    app.register_blueprint(auth)


loader_meta.priority = 1.0
