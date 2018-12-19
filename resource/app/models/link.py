#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db
from datetime import datetime

class Link(db.Model):
    """ 链接模型 """
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    md5 = db.Column(db.String(32), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    type_id = db.Column(db.Integer, db.ForeignKey('media_type.id'))

    def __repr__(self):
        return '<Link %r>' % self.name