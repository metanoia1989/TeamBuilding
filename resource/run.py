#!/usr/bin/env python3
# -*- conding:utf8 -*-

import os 
from app import create_app, db
from app.models import (User, Role, Permission, Category, Resource, 
                        Like, Link, MediaType, Project, ProjectResource)
from flask_migrate import Migrate
import logging 
from config import config


logging.basicConfig(filename='./log/resource.log', level=logging.INFO)
app = create_app(os.getenv('FlASK_CONFIG') or 'default')
migrate  = Migrate(app, db)

# # 集成 Python shell
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
