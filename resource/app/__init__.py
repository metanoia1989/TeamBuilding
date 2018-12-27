#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Flask
from config import config
from os import getenv
from logging import basicConfig, INFO, info
from datetime import date

def register_blueprint(app):
    from app.api import api_blueprint
    app.register_blueprint(api_blueprint)

def register_extensions(app):
    from app.extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

def init_log():
    today_str = date.today().strftime('%Y-%m-%d')
    basicConfig(filename='./log/resource-' + today_str + '.log', level=INFO)

def start_remote_debug():
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.close()
        import ptvsd
        ptvsd.enable_attach(address=('0.0.0.0', 8000), redirect_output=True)
        print('ptvsd is started')
        # ptvsd.wait_for_attach()
        # print('debugger is attached')
    except OSError as exc:
        print('ptvsd not started')
        print(exc)

def create_app(config_name):
    """
    初始化app，注册蓝图，注册扩展，启动日志
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprint(app)
    register_extensions(app)
    init_log()

    return app

app = create_app(getenv('FlASK_CONFIG') or 'default')