#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app import app
from app.extensions import db
from app.models.permission import Permission
from app.models.user import User
from app.models.role import Role
from app.lib.fake import FakerData
from app.lib.command import init_db


@app.shell_context_processor
def make_shell_context():
    """集成 Python shell""" 
    return dict(app=app, db=db, Permission=Permission, User=User, Role=Role, FakerData=FakerData)


if __name__ == '__main__':
    # if(getenv('FLASK_DEBUG') == 1):
    app.run(host='0.0.0.0', port=8888, debug=True)
