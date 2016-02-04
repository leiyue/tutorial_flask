# -*- coding: utf-8 -*-
# @Date    : 2016-01-31 12:42
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_debugtoolbar import DebugToolbarExtension

from .app import create_app

db = SQLAlchemy()
toolbar = DebugToolbarExtension()

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)


def config_extensions(app):
    """ initialize application
    :param app:
    :return:
    """
    db.init_app(app)
    toolbar.init_app(app)
