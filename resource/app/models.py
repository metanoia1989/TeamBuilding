#!/usr/bin/env python3
# -*- conding:utf8 -*-

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import hashlib
from flask import current_app, request, url_for

class User(db.Model):
    """ User表模型 """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    # 用户资料
    name = db.Column(db.String(64)) # 真实姓名
    location = db.Column(db.String(64)) # 所在地
    about_me = db.Column(db.Text()) # 自我介绍
    member_since = db.Column(db.DateTime(), default=datetime.utcnow) # 注册日期
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow) # 最后访问日期
    avatar_hash = db.Column(db.String(32)) # 头像

    # 关联
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    resources = db.relationship('Resource', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        # 使用缓存的md5散列值生成 Gravatar URL 
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.name

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    # 确认账号
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try: 
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # 生成重置密码token
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    # 生成gravatar默认头像
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    # 生成令牌 验证令牌
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

class Role(db.Model):
    """ 角色模型 """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    permissions = db.Column(db.String(255) )
    default = db.Column(db.Boolean, default=False, index=True)

    @staticmethod
    def insert_roles():
        roles = {
            'User': [],
            'Moderator': [],
            'Administrator': []
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name

class Permission(db.Model):
    """ 权限模型 """
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return '<Permission %r>' % self.name

class Category(db.Model):
    """ 标签模型 """
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    resources = db.relationship('Resource', backref='resource', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name

class Resource(db.Model):
    """ 资源模型 """
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    body_md = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    pin = db.Column(db.Integer, default=False)
    hot = db.Column(db.Integer, default=False)
    clicks = db.Column(db.Integer, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<Resource %r>' % self.title

class Like(db.Model):
    """ 点赞模型 """
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.Integer, default=False)
    unlike = db.Column(db.Integer, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('resources.id'))

    def __repr__(self):
        return '<Like %r>' % self.id

class Link(db.Model):
    """ 链接模型 """
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    md5 = db.Column(db.String(32), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    type_id = db.Column(db.Integer, db.ForeignKey('media_type.id'))

    def __repr__(self):
        return '<Link %r>' % self.name

class MediaType(db.Model):
    """ 资源类型模型 """
    __tablename__ = 'media_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    links = db.relationship('Link', backref='link', lazy='dynamic')

    def __repr__(self):
        return '<MediaType %r>' % self.name

class Project(db.Model):
    """ 资源专题模型 """
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(2083))
    slug = db.Column(db.String(100), default='')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    resources = db.relationship('Resource', backref='project', lazy='dynamic')

    def __repr__(self):
        return '<Project %r>' % self.name

class ProjectResource(db.Model):
    """ 专题资源关联模型 """
    __tablename__ = 'project_resources'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

