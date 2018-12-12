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
        """设置用户id为1的为站长，id小于10的为管理员"""
        role_ids = Role.query.with_entities(Role.id).all()
        role_ids = [ x[0] for x in role_ids ]
        faker_users = [User(
            email = fake_zh.email(),
            username = fake_en.name(),
            password_hash = generate_password_hash('123456'),
            confirmed = random.choice([1, 1, 1, 1, 0]),
            name = fake_zh.name(),
            location = fake_zh.address(),
            about_me = fake_zh.text(max_nb_chars=100),
            role_id = random.choice(role_ids)
        ) for _ in range(num)]
        db.session.add_all(faker_users)
        db.session.commit()

    @staticmethod
    def make_permission():
        """创建权限，以及插入角色对应的权限"""
        pass

    @staticmethod
    def make_category():
        """创建资源标签"""
        pass

    @staticmethod
    def make_mediatype():
        """创建媒体资源类型"""
        pass

    @staticmethod
    def make_resource(num=1000):
        """创建资源"""
        pass

    @staticmethod
    def make_project(num=100):
        """创建资源专题，以及专题对应的资源"""
        pass