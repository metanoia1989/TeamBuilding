#!/usr/bin/env python3
# -*- coding: utf-8  -*-

from app import app
from app.lib.fake import FakerData
import click

@app.cli.command()
def init_db():
    """
    初始化数据库数据
    """
    FakerData.make_role()
    FakerData.make_user()
    FakerData.set_role()
    FakerData.make_permission()
    FakerData.assign_permission()
    FakerData.make_category()
    FakerData.make_mediatype()
    FakerData.make_resource()
    FakerData.make_project()
    FakerData.assign_resource()
