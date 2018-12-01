#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import os, os.path, sys
import logging
import config

def test_config():
    config_name = os.getenv('FLASK_CONFIG') or 'default'
    logging.basicConfig(filename='../log/resource.log', level=logging.INFO)
    logging.info(config_name)

