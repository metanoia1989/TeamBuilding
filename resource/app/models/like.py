#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db
from app.models.base import Model

class Like(Model):
    """ 点赞模型 """
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    like = db.Column(db.Integer, default=False)
    unlike = db.Column(db.Integer, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

    def __repr__(self):
        return '<Like %r>' % self.id