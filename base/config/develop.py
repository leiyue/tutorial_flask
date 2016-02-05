# -*- coding: utf-8 -*-
# @Date    : 2016-01-31 12:34
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

""" Development settings must be here.
"""

from .production import *

DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG_TB_INTERCEPT_REDIRECTS = False
