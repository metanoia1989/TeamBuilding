#!/usr/bin/env python3
# -*- conding:utf8 -*-

import os.path, os
import pickle

imgs_dir = os.path.abspath(os.path.dirname(__file__) + os.path.sep +  '../app/static/img/')
file_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + 'imgPaht.txt')
imgs_path = os.listdir(imgs_dir)
paths = [ 'img' + os.path.sep + path for path in imgs_path]

with open(file_path, 'wb') as f:
    pickle.dump(paths, f, 0)
    print("序列化成功")