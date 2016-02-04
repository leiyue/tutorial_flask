# -*- coding: utf-8 -*-
# @Date    : 2016-01-31 12:26
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from flask import Flask

from .config import production


def create_app(config=None, **skip):
    """ create flask application
    :param config: configuration class
    :param skip:
    :return app: application instance
    """
    app = Flask(__name__)
    app.config.from_object(config or production)

    # with app.test_request_context():

    from .ext import config_extensions
    config_extensions(app)

    from .loader import loader
    loader.register(app)

    return app


# @app.route('/')
# def hello_world():
#     return 'Hello World!
