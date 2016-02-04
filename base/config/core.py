# -*- coding: utf-8 -*-
# @Date    : 2016-01-31 12:31
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

""" Core configuration settings.
"""

from base.config import op, ROOT_DIR

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + op.join(ROOT_DIR, '.db')

# WTForms
CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"
