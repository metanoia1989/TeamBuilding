
from app.exceptions import ValidationError, ApiException

class Success(ApiException):
    code = 201
    error_code = 0
    msg = 'Create ok'

class ExecuteSuccess(ApiException):
    code = 204
    error_code = 1
    msg = 'Execute ok'

class ServerError(ApiException):
    code = 500
    error_code = 999
    msg = 'Sorry, server has a mistake!'

class ParameterException(ApiException):
    code = 400
    error_code = 1000
    msg = 'Invalid parameter'

class NotFound(ApiException):
    code = 404
    error_code = 1001
    msg = 'The resource are not found 0_0...'

class AuthFailed(ApiException):
    code = 401
    error_code = 1005
    msg = 'Authorization failed'

class Forbidden(ApiException):
    code = 403
    error_code = 1004
    msg = 'Forbidden access'