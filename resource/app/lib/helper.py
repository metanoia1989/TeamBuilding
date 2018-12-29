#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.models.role import Role
from app.lib.cache import Cache

def get_permissions(pclass='api'):
    """
    获取所有角色和权限关联数据
    """
    roles = Role.query.all()
    data = Cache.get('{}_permissions'.format(pclass)) 
    if data is None:
        data = {}
    else:
        return data
    for role in roles:
        permissions = [ p.dict() for p in role.permissions.filter_by(pclass=pclass).all()]
        permissions = map(lambda p: (p.get('pclass').lower() + '.' + p.get('sources').lower(), p.get('action')) , permissions)
        data[role.id] = list(permissions)
    Cache.set('{}_permissions'.format(pclass), data)
    return data
