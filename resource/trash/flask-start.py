#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Hello World</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)