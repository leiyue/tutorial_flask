# -*- coding: utf-8 -*-
# @Date    : 2016-01-31 13:02
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from base.ext import db, manager
from base.loader import loader

loader.register(manager, submodule='manage')


@manager.shell
def make_shell_context():
    from flask import current_app
    return dict(app=current_app, db=db)


if __name__ == '__main__':
    manager.run()
