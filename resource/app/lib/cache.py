#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import time

class Cache(object):
    _cache_ = {}
    VALUE = 0
    EXPIRES = 1

    @classmethod
    def get(cls, key):
        """
        根据key获取缓存的值
        """
        try:
            if cls._cache_[key][cls.EXPIRES] > time.time():
                return cls._cache_[key][cls.VALUE]
            else:
                del cls._cache_[key]
                return None
        except KeyError:
            return None

    @classmethod
    def set(cls, key, value, duration=3600):
        """
        储存覆盖键为key的值
        """
        try:
            expires = time.time() + duration
        except TypeError:
            raise TypeError("Duration must be numeric")

        cls._cache_[key] = (value, expires)
        return cls.get(key)

    @classmethod
    def clean(cls):
        """
        移除所有过期的缓存值
        """
        for key in cls._cache_.keys():
            cls.get(key)

    @classmethod
    def purge(cls):
        """
        移除所有的缓存值
        """
        cls._cache_ = {}