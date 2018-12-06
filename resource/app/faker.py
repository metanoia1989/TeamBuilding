#!/usr/bin/env python3
# -*- conding:utf8 -*-

from faker import Factory
from .models import (
    User, Role, Permission, 
    Resource, Category, Project, 
    ProjectResource, Like, Link, MediaType
)
from . import db
from sqlalchemy.exc import IntegrityError

fake = Factory.create()


