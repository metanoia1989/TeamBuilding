#!/usr/bin/env python3
# -*- coding: utf-8  -*-


from flask import request, json
from werkzeug.exceptions import HTTPException


class ValidationError(ValueError):
    pass

class ApiException(HTTPException):
    code = 500
    msg = 'sorry, server has a mistake'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg: 
            self.msg = msg
        return super(ApiException, self).__init__(msg, None)
    
    def get_body(self, environ=None):
        content = {
            'msg': self.msg,
            'error_code': self.error_code,
            'request': request.method + ' ' + request.base_url
        }
        return json.dumps(content)

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]