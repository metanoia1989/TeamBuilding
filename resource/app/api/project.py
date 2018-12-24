#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import abort
from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from app.api import api, meta_fields
from app.extensions import auth
from app.models.project import Project 
from app.models.role import Role
from app.lib.errors import success, execute_success
from app.lib.decorators import paginate

# 请求字段过滤
project_parser = reqparse.RequestParser()
project_parser.add_argument('email', type=inputs.regex('^\w([+-.]\w+)*@\w+\.\w+$'), trim=True, required=True, help='邮箱不合标准')
project_parser.add_argument('projectname', type=str, required=True, trim=True, help='必须填写用户名')
project_parser.add_argument('password_hash', type=str, required=True, trim=True, help='必须填写密码')
project_parser.add_argument('confirmed', type=bool, default=1)
project_parser.add_argument('name', type=str)
project_parser.add_argument('location', type=str)
project_parser.add_argument('about_me', type=str)
project_parser.add_argument('member_since', type=int)
project_parser.add_argument('role_id', type=int, choices=Role.get_role_ids())
# args = project_parser.parse_args() # 解析参数

# 格式化输出
project_fields = {
    'id': fields.Integer,
    'role_id':fields.Integer, 
    'email': fields.String,
    'projectname': fields.String,
    'confirmed': fields.Boolean,
    'name': fields.String,
    'about_me': fields.String,
    'avatar_hash': fields.String,
}

project_collection_fields = {
    'items': fields.List(fields.Nested(project_fields)),
    'meta': fields.Nested(meta_fields),
}

class Project(Resource):
    decorators = [auth.login_required]

    @marshal_with(project_fields)
    def get(self, id=None):
        project = Project.query.filter_by(id=id).first()
        if not project:
            abort(404)
        return project
    
    def delete(self, id=None):
        project = Project.query.filter_by(id=id).first()
        if not project:
            abort(404)
        project.delete()
        return execute_success()
    
    def post(self):
        args = project_parser.parse_args()
        # project owns the task
        args['author_id'] = g.current_project.id
        project = Project.create(**args)
        return success()

    def put(self, id=0, **kwargs):
        project = Project.query.filter_by(id=id).first()
        if not project:
            abort(404)
        project.update(**project_parser.parse_args())
        return execute_success()

class ProjectCollection(Resource):
    decorators = [auth.login_required]

    @marshal_with(project_collection_fields)
    @paginate(10)
    def get(self, project_id=None):
        projects = Project.query
        if project_id:
            project = Project.query.filter_by(id=project_id).first()
            if project is None:
                abort(404)
            projects = Project.query.filter_by(author_id=project.id) 
        return projects

    
api.add_resource(Project, '/project' ,'/project/<int:id>', endpoint='project')
api.add_resource(ProjectCollection, '/projects' ,'/projects/<int:project_id>', endpoint='projects')