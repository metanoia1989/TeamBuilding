#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Flask
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprint(app)
    register_extensions(app)

    return app

def register_blueprint(app):
    from app.api import api_blueprint
    app.register_blueprint(api_blueprint)

def register_extensions(app):
    from app.extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)