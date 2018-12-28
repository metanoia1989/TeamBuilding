#!/usr/bin/env python3
# -*- coding: utf-8  -*-

from app.api import api_blueprint
from app.lib.cache import Cache

@api_blueprint.route('/set_value/<string:key>/<string:value>')
def set_value(key, value):
    Cache.set(key, value)
    return '设置成功'

@api_blueprint.route('/get_value/<string:key>')
def get_value(key):
    value = Cache.get(key)
    print(value)
    return 'he llo'

