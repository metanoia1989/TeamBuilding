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

class FakerData():

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
        """生成虚拟用户，= = 好像超过100个时候，邮箱就会重复"""
        role_id = Role.query.filter_by(name='普通用户').first().id
        faker_users = [User(
            email = fake_zh.email(),
            username = fake_en.name(),
            password_hash = generate_password_hash('123456'),
            confirmed = random.choice([1, 1, 1, 1, 0]),
            name = fake_zh.name(),
            location = fake_zh.address(),
            about_me = fake_zh.text(max_nb_chars=100),
            role_id = role_id
        ) for _ in range(num)]

        for user in faker_users:
            try:
                db.session.add(user)
            except IntegrityError as e:
                db.session.rollback()
                continue
        db.session.commit()

    @staticmethod
    def set_role():
        """设置第一个用户为站长，id小于20的为管理员"""
        siter_id = Role.query.filter_by(name='站长').first().id
        siter_user = User.query.first()
        siter_user.role_id = siter_id
        siter_user.confirmed = 1
        db.session.add(siter_user)

        admin_id = Role.query.filter_by(name='版主').first().id
        admin_users = User.query.limit(10).offset(1).all() 
        for admin_user in admin_users:
            admin_user.role_id = admin_id
            admin_user.confirmed = 1
        db.session.add_all(admin_users)

        db.session.commit()

    @staticmethod
    def make_permission():
        """
        创建权限，以及插入角色对应的权限
        """
        permissions = [
            { 'name': '用户管理', 'sources': 'User', 'action': 'all' },
            { 'name': '角色管理', 'sources': 'Role', 'action': 'all' },
            { 'name': '权限管理', 'sources': 'Permission', 'action': 'all' },
            { 'name': '资源管理', 'sources': 'Resource', 'action': 'all' },
            { 'name': '标签管理', 'sources': 'Category', 'action': 'all' },
            { 'name': '专题管理', 'sources': 'Project', 'action': 'all' },
            { 'name': '媒体类型管理', 'sources': 'MediaType', 'action': 'all' },
            { 'name': '资源链接管理', 'sources': 'Link', 'action': 'all' },
        ]
        for p in permissions:
            permission = Permission.query.filter_by(name=p.get('name')).first()
            if permission is not None:
                continue
            permission = Permission(**p)
            db.session.add(permission)
        db.session.commit()

    @staticmethod
    def assign_permission():
        """为角色分配权限"""


    @staticmethod
    def make_category(num=100):
        """创建资源标签"""
        names = tuple([fake_zh.word() for _ in range(num)])
        for name in names:
            category = Category.query.filter_by(name=name).first()
            if category is not None:
                continue
            category = Category(name=name)
            db.session.add(category)
        db.session.commit()

    @staticmethod
    def make_mediatype():
        """创建媒体资源类型"""
        names = ['链接', '图片', '视频', '音频', '附件']
        for name in names:
            mediatype = MediaType.query.filter_by(name=name).first()
            if mediatype is not None:
                continue
            mediatype = MediaType(name=name)
            db.session.add(mediatype)
        db.session.commit()

    @staticmethod
    def make_resource(num=100):
        """创建资源"""
        author_ids = User.query.filter(User.confirmed==1).with_entities(User.id).all()
        author_ids = [ x[0] for x in author_ids ]
        category_ids = Category.query.with_entities(Category.id).all()
        category_ids = [ x[0] for x in category_ids ]
        for _ in range(num):
            resource = Resource() 
            resource.title = fake_zh.sentence(nb_words=7, variable_nb_words=True)
            resource.body_md = fake_zh.text(max_nb_chars=700)
            resource.author_id = random.choice(author_ids)
            resource.category_id = random.choice(category_ids)
            db.session.add(resource)
        db.session.commit()

    @staticmethod
    def make_project(num=100):
        """创建资源专题，以及专题对应的资源"""
        pass

    @staticmethod
    def assign_resource(num=100):
        """分配专题的相关资源"""
        pass