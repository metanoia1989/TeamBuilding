#!/usr/bin/env python3
# -*- conding:utf8 -*-


from app.models.resource import Resource as Resource_Model
from flask_restful import Resource 

class Resources(Resource):
    def get(self):
        return {'hello': 'world'}