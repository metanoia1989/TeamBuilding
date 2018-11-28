#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Flask
from flask_restful import Api
from example.resources.foo import Foo
from example.resources.bar import Bar
from example.resources.baz import Baz

app = Flask(__name__)
api = Api(app)

api.add_resource(Foo, '/Foo', '/Foo/<str:id>')
api.add_resource(Bar, '/Bar', '/Bar/<str:id>')
api.add_resource(Baz, '/Baz', '/Baz/<str:id>')