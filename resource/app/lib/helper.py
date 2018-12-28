#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.models.role import Role

def get_permissions(type='api'):
    """
    获取所有角色和权限关联数据
    """
    roles = Role.query.all()
    data = {}
    for role in roles:
        permissions = [ p.dict() for p in role.permissions.filter_by(type=type).all()]
        data[role.id] = permissions
    return data
