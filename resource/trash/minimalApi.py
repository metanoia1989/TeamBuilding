#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    
api.add_resource(HelloWorld, '/', '/hello')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)