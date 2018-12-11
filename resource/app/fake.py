#!/usr/bin/env python3
# -*- conding:utf8 -*-

from faker import Factory
from .models import (
    User, Role, Permission, 
    Resource, Category, Project, 
    ProjectResource, Like, Link, MediaType
)
from . import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
import random

fake_zh = Factory.create('zh_TW')
fake_en = Factory.create('en_US')

class MakeFakerData():

    @staticmethod
    def make_role():
        roles = [
            { 'name': '站长' },
            { 'name': '版主' },
            { 'name': '普通用户', 'default': 1 },
        ]
        for r in roles:
            role = Role.query.filter_by(name=r.get('name')).first()
            if role is not None:
                continue
            role = Role(name=r.get('name'))
            role.default = (role.name == '普通用户')
            db.session.add(role)
        db.session.commit()

    @staticmethod
    def make_user(num = 100):
        faker_users = [User(
            email = fake_zh.email(),
            username = fake_en.name(),
            password_hash = generate_password_hash('123456'),
            confirmed = random.choice([1, 1, 1, 1, 0]),
            name = fake_zh.name(),
            location = fake_zh.address(),
            about_me = fake_zh.text(max_nb_chars=100),
            role_id = random.choice([])
        ) for _ in range(num)]
        db.session.add_all(faker_users)
        db.session.commit()