#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import hashlib
from flask import current_app, request, url_for

class User(db.Model):
    """ User表模型 """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    # 用户资料
    name = db.Column(db.String(64), comment='真实姓名')
    location = db.Column(db.String(64), comment='所在地') 
    about_me = db.Column(db.Text(), comment='自我介绍') 
    member_since = db.Column(db.DateTime(), default=datetime.utcnow, comment='注册日期') 
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow, comment='最后访问日期') 
    avatar_hash = db.Column(db.String(32), comment='头像')  

    # 关联
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
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
        return s.dumps({'id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

""" 角色权限表 """
RolePermission = db.Table('role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
)

class Role(db.Model):
    """ 角色模型 """
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False, comment='角色名')
    default = db.Column(db.Boolean, default=0, index=True, comment='是否为默认角色')
    permissions = db.relationship('Permission', secondary=RolePermission, lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            '普通用户': [],
            '管理员': [],
            '站长': []
        }
        default_role = '普通用户'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        pass

    def remove_permission(self, perm):
        pass

    def reset_permissions(self):
        pass

    def has_permission(self, perm):
        pass

    def __repr__(self):
        return '<Role %r>' % self.name

class Permission(db.Model):
    """ 权限模型 """
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False, comment='权限名')
    sources = db.Column(db.String(64), nullable=False, comment='资源名 与数据表对应')
    action = db.Column(db.String(64), nullable=False, comment='动作 all, add, update, delete, query')

    def __repr__(self):
        return '<Permission %r>' % self.name

class Category(db.Model):
    """ 标签模型 """
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False, comment='标签名')
    resources = db.relationship('Resource', backref='resource', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name

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

class Like(db.Model):
    """ 点赞模型 """
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    like = db.Column(db.Integer, default=False)
    unlike = db.Column(db.Integer, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

    def __repr__(self):
        return '<Like %r>' % self.id

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

class MediaType(db.Model):
    """ 资源类型模型 """
    __tablename__ = 'media_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    links = db.relationship('Link', backref='media_type', lazy='dynamic')

    def __repr__(self):
        return '<MediaType %r>' % self.name

""" 专题资源关联模型 """
ProjectResource = db.Table('project_resource',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id')),
    db.Column('create_time' ,db.DateTime, default=datetime.utcnow)
)

class Project(db.Model):
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

