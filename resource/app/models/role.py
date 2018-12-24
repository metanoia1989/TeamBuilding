#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db
from app.models.relationship import RolePermission
from datetime import datetime
from app.models.base import CRUDMixin

class Role(CRUDMixin, db.Model):
    """ 角色模型 """
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False, comment='角色名')
    default = db.Column(db.Boolean, default=0, index=True, comment='是否为默认角色')
    permissions = db.relationship('Permission', secondary=RolePermission, lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            '普通用户': [],
            '管理员': [],
            '站长': []
        }
        default_role = '普通用户'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    @staticmethod
    def get_role_ids():
        role_ids = Role.query.filter(Role.confirmed==1).with_entities(Role.id).all()
        role_ids = [ x[0] for x in role_ids ]
        return role_ids

    def add_permission(self, perm):
        pass

    def remove_permission(self, perm):
        pass

    def reset_permissions(self):
        pass

    def has_permission(self, perm):
        pass

    def __repr__(self):
        return '<Role %r>' % self.name