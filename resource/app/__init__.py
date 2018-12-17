#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from config import config
import logging

db = SQLAlchemy()

def register_blueprint(app):
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    register_blueprint(app)

    return app