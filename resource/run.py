#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app import create_app
from app.extensions import db
from app.models.permission import Permission
from app.models.user import User
from app.models.role import Role
from app.lib.fake import FakerData
from config import config
from logging import basicConfig, INFO, info
from os import getenv
from datetime import date
# import ptvsd

# ptvsd.enable_attach(address=('0.0.0.0', 8899), redirect_output=True)

app = create_app(getenv('FlASK_CONFIG') or 'default')
today_str = date.today().strftime('%Y-%m-%d')
basicConfig(filename='./log/resource-' + today_str + '.log', level=INFO)


# 集成 Python shell
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Permission=Permission, User=User, Role=Role, FakerData=FakerData)


if __name__ == '__main__':
    # if(getenv('FLASK_DEBUG') == 1):
    app.run(host='0.0.0.0', port=8888, debug=True)
