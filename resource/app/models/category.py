#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db

class Category(db.Model):
    """ 标签模型 """
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False, comment='标签名')
    resources = db.relationship('Resource', backref='resource', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name
