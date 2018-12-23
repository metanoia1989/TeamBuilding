#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db
from datetime import datetime
from app.models.base import CRUDMixin

class MediaType(CRUDMixin, db.Model):
    """ 资源类型模型 """
    __tablename__ = 'media_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    links = db.relationship('Link', backref='media_type', lazy='dynamic')

    def __repr__(self):
        return '<MediaType %r>' % self.name