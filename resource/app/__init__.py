#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()