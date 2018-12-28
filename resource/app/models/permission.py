#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db
from datetime import datetime
from app.models.base import Model

class Permission(Model):
    """ 权限模型 """
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False, comment='权限名')
    type = db.Column(db.String(10), unique=True, nullable=False, comment='权限类型')
    sources = db.Column(db.String(64), nullable=False, comment='资源名 与数据表对应')
    action = db.Column(db.String(64), nullable=False, comment='动作 all, add, update, delete, query')

    def __repr__(self):
        return '<Permission %r>' % self.name