# -*- coding: utf-8 -*-
# @Date    : 2016-01-31 12:32
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

""" Production settings must be here.
"""

from .core import *

SECRET_KEY = 'SecretKeyForSessionSigning'

COLLECT_STATIC_ROOT = op.join(op.dirname(ROOT_DIR), 'static')
