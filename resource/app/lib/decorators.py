#!/usr/bin/env python3
# -*- conding:utf8 -*-

from functools import wraps
from flask import g, request, jsonify
from app.lib.errors import forbidden_error, server_error
from app.lib.helper import get_permissions

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


def api_permission_control():
    def access_control(func):
        def wrap_func(*args, **kwargs):
            try:
                endpoint = request.endpoint
                http_method = request.method.lower()
                role_id = g.current_user.role_id
                permissions =  get_permissions(pclass='api').get(role_id)
                permissions = map(lambda x: (x.get('pclass').lower() + '.' + x.get('sources').lower(), x.get('action')) , permissions)
                for p in permissions:
                    if endpoint == p[0] and p[1] == 'all':
                        return func(args, **kwargs)
                    if endpoint == p[0] and http_method == p[1]:
                        return func(args, **kwargs)
                return forbidden_error('no permission')
            except KeyError:
                return forbidden_error('no permission')
            except Exception as e:
                return server_error('api permission control error,error msg %s' % str(e))
            return wrap_func
        return access_control