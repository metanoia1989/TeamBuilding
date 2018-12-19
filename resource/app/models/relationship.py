#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db
from datetime import datetime

""" 角色权限表 """
RolePermission = db.Table('role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
)

""" 专题资源关联模型 """
ProjectResource = db.Table('project_resource',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id')),
    db.Column('create_time' ,db.DateTime, default=datetime.utcnow)
)