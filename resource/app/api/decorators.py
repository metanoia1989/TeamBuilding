#!/usr/bin/env python3
# -*- conding:utf8 -*-

from functools import wraps
from flask import g
from .errors import forbidden_error

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden_error('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator