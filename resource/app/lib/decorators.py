#!/usr/bin/env python3
# -*- conding:utf8 -*-

from functools import wraps
from flask import g, request
from app.lib.errors import forbidden_error

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden_error('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def paginate(max_per_page=20):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', max_per_page,
                                            type=int),
                           max_per_page)

            query = func(*args, **kwargs)
            p = query.paginate(page, per_page)

            meta = {
                'page': page,
                'per_page': per_page,
                'total': p.total,
                'pages': p.pages,
            }

            result = {
                'items': p.items,
                'meta': meta
            }

            return result, 200
        return wrapped
    return decorator