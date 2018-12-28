#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import os 
import errno
import sqlite3 
import sys
from time import time
from cPickle import loads, dumps

import logging

logger = logging.getLogger(__name__)

class SqliteCache:
    """
    使用sqlite3实现的持久化缓存类
    """
    _create_sql = (
        'CREATE TABLE IF NOT EXISTS entries '
        '( key TEXT PRIMARY KEY, val BLOB, exp FLOAT )'
    )
    _create_index = 'CREATE INDEX IF NOT EXISTS keyname_index ON entries (key)'
    _get_sql = 'SELECT val, exp FROM entries WHERE key = ?'
    _del_sql = 'DELETE FROM entries WHERE key = ?'
    _set_sql = 'REPLACE INTO entries (key, val, exp) VALUES (?, ?, ?)'
    _add_sql = 'INSERT INTO entries (key, val, exp) VALUES (?, ?, ?)'
    _clear_sql = 'DELETE FROM entries'

    connection = None

    def __init__(self, path):
        """初始化 SqliteCache 实例"""
        self.path = os.path.abspath(path)
        logger.debug('实例化缓存数据库路径 {path}'.format(path=self.path))
        # 创建缓存数据库目录
        try:
            os.mkdir(self.path)
            logger.debug('成功创建缓存数据库路径 {path}'.format(path=self.path))
        except OSError as e:
            if e.errno != errno.EEXIST or not os.path.isdir(self.path):
                raise
            
    def _get_conn(self):
        """返回sqlite连接实例"""
        if self.connection:
            return self.connection

        cache_db_path = os.path.join(self.path, 'cache.sqlite')
        conn = sqlite3.Connection(cache_db_path, timeout=60)
        logger.debug('已连接 {path}'.format(path=cache_db_path))

        with conn:
            conn.execute(self._clear_sql)
            conn.execute(self._create_index)
            logger.debug('创建表和索引成功')

        self.connection = conn
        return self.connection
            

    def get(self, key):
        """从缓存中取出值"""
        return_value = None

        with self._get_conn() as conn:
            for row in conn.execute(self._get_sql, (key, )):
                expire = row[1]
                if expire == 0 or expire > time():
                    return_value = loads(str(row[0]))
                    # TODO: Delete the value that is expired?
                break
        return return_value

    def set(self, key, value, timeout=None):
        """
        添加一个键值对，并且附加过期时间
        """
        expire = 0 if not timeout else time() + timeout
        # serialize the value with protocol 2
        data = memoryview(dumps(value, 2))
        with self._get_conn() as conn:
            try:
                conn.execute(self._add_sql, (key, data, expire))
            except sqlite3.IntegrityError:
                logger.warning('试图添加已存在的键 {k}，进行更新操作'.format(k=key))
                self.update(key, value, timeout)
            
    def update(self, key, value, timeout=None):
        """
        更新一个键值对，并且附加过期时间
        """
        expire = 0 if not timeout else time() + timeout
        # serialize the value with protocol 2
        data = memoryview(dumps(value, 2))
        with self._get_conn() as conn:
            conn.execute(self._set_sql, (key, data, expire))

    def delete(self, key):
        """删除一个键值对"""
        with self._get_conn() as conn:
            conn.execute(self._del_sql, (key,))

    def delete(self, key):
        """清除所有键值对"""
        with self._get_conn() as conn:
            conn.execute(self._clear_sql)

    def __del__(self):
        """对象被回收时，关闭sqlite连接"""
        if self.connection:
            self.connection.close()

                 