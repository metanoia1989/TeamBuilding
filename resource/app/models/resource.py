#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db
from datetime import datetime


class Resource(db.Model):
    """ 资源模型 """
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    body_md = db.Column(db.Text, comment='markdown文本')
    body_html = db.Column(db.Text, comment='html文本')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    pin = db.Column(db.Integer, default=False, comment='置顶')
    hot = db.Column(db.Integer, default=False, comment='热门')
    clicks = db.Column(db.Integer, default=False, comment='点击量')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='作者')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), comment='标签')

    def __repr__(self):
        return '<Resource %r>' % self.title