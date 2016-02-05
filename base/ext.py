# -*- coding: utf-8 -*-
# @Date    : 2016-01-31 12:42
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from flask_script import Manager
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_collect import Collect

from .app import create_app

db = SQLAlchemy()
toolbar = DebugToolbarExtension()
migrate = Migrate()

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command('db', MigrateCommand)

collect = Collect()
collect.init_script(manager)


def config_extensions(app):
    """ initialize application
    :param app:
    :return:
    """
    db.init_app(app)
    toolbar.init_app(app)
    collect.init_app(app)
    migrate.init_app(app, db)
