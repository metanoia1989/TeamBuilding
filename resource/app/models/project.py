#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db
from app.models.base import Model
from app.models.relationship import ProjectResource
from datetime import datetime

class Project(Model):
    """ 资源专题模型 """
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(2083))
    slug = db.Column(db.String(100), default='')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    resources = db.relationship('Resource', secondary=ProjectResource, 
                                backref=db.backref('projects', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Project %r>' % self.name