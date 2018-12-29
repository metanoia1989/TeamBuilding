#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import abort
from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from app.api import api, meta_fields
from app.api.resources import resource_fields
from app.extensions import auth
from app.models.project import Project as ProjectModel 
from app.lib.errors import success, execute_success 
from app.lib.decorators import paginate, api_permission_control

# 请求字段过滤
project_parser = reqparse.RequestParser()
project_parser.add_argument('name', type=str)
project_parser.add_argument('cover', type=inputs.regex('^.+\.(jpg|gif|png)$'))
project_parser.add_argument('slug', type=str)
# args = project_parser.parse_args() # 解析参数

# 格式化输出
project_fields = {
    'id': fields.Integer,
    'name':fields.String, 
    'cover': fields.String,
    'slug': fields.String,
    'timestamp': fields.String,
    'resources': fields.List(fields.Nested(resource_fields)),
}

project_collection_fields = {
    'items': fields.List(fields.Nested(project_fields)),
    'meta': fields.Nested(meta_fields),
}

class ProjectApi(Resource):
    method_decorators = {
        'delete': [api_permission_control(), auth.login_required], 
        'post': [api_permission_control(), auth.login_required],
        'put': [api_permission_control(), auth.login_required],
    }

    @marshal_with(project_fields)
    def get(self, id=None):
        project = ProjectModel.query.filter_by(id=id).first()
        if not project:
            abort(404)
        return project
    
    def delete(self, id=None):
        project = ProjectModel.query.filter_by(id=id).first()
        if not project:
            abort(404)
        project.delete()
        return execute_success()
    
    def post(self):
        args = project_parser.parse_args()
        # project owns the task
        project = ProjectModel.create(**args)
        return success()

    def put(self, id=0, **kwargs):
        project = ProjectModel.query.filter_by(id=id).first()
        if not project:
            abort(404)
        project.update(**project_parser.parse_args())
        return execute_success()

class ProjectCollectionApi(Resource):

    @marshal_with(project_collection_fields)
    @paginate(10)
    def get(self, project_id=None):
        projects = ProjectModel.query
        return projects
    
api.add_resource(ProjectApi, 'project' ,'/project/<int:id>', endpoint='project')
api.add_resource(ProjectCollectionApi, '/projects' , endpoint='projects')