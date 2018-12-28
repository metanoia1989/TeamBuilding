#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.extensions import db
from sqlalchemy.orm import relationship
from flask_sqlalchemy import BaseQuery
from sqlalchemy.ext.declarative import DeclarativeMeta

import json

class CRUDMixin:
    """
    Mixin that adds convenience methods for CRUD (create, read, update, delete) operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        # Prevent changing ID of object
        kwargs.pop('id', None)
        for attr, value in kwargs.items():
            # Flask-RESTful makes everything None by default :/
            if value is not None:
                setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True
    __exclude__ = []
    __include__ = []
    __exclude_foreign__ = True

    def dict(self):
        data = {}
        for field in self.__fields__():
            value = getattr(self, field)  # value
            if isinstance(value.__class__, DeclarativeMeta):
                data[field] = value.dict()
            elif not hasattr(value, '__func__') and not isinstance(value, BaseQuery):
                try:
                    data[field] = value
                except TypeError:
                    data[field] = None
        return data

    def json(self):
        data = {}
        for field in self.__fields__():
            value = getattr(self, field)  # value
            if isinstance(value.__class__, DeclarativeMeta):
                data[field] = value.dict()
            elif not hasattr(value, '__func__') and not isinstance(value, BaseQuery):
                try:
                    json.dumps(value)
                    data[field] = value
                except TypeError:
                    try:
                        data[field] = str(value)
                    except Exception as e:
                        data[field] = None
        return json.dumps(data)

    def __foreign_column__(self):
        data = []
        for column in self.__table__.columns:
            if getattr(column, 'foreign_keys'):
                data.append(column.key)
        return data

    def __fields__(self):
        fields = set(dir(self))
        if self.__exclude_foreign__:
            fields = fields - set(self.__foreign_column__())
        fields = fields - set(self.__exclude__)
        fields = set(list(fields) + self.__include__)
        return [f for f in fields if
                not f.startswith('_') and not f.endswith('_id') and f not in ['metadata', 'query', 'query_class',
                                                                              'dict', 'json']]


class SurrogatePK:
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if id <= 0:
            raise ValueError('ID must not be negative or zero!')
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None