#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app import app, start_remote_debug
from app.extensions import db
from app.models.permission import Permission
from app.models.user import User
from app.models.role import Role
from app.lib.fake import FakerData
from app.lib.command import init_db
from dotenv import find_dotenv, load_dotenv
import os

# 加载 .env 为环境变量
load_dotenv(find_dotenv())

@app.shell_context_processor
def make_shell_context():
    """集成 Python shell""" 
    return dict(app=app, db=db, Permission=Permission, User=User, Role=Role, FakerData=FakerData)


if __name__ == '__main__':
    if int(os.environ.get('FLASK_REMOTE_DEBUG')):
        start_remote_debug()   
    debug = int(os.environ.get('FLASK_DEBUG', 0))
    app.run(host='0.0.0.0', port=8888, debug=debug)
