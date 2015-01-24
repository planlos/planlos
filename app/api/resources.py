from flask.ext.restful import Resource
from functools import wraps
from flask import make_response, jsonify


def jsend():
    def jsend_decorator(func):
        @wraps(func)
        def wrapper(data, status='success', message=None):
            if message is not None:
                result = dict(data=data, status=status, message=message)
            else:
                result = dict(data=data, status=status)
            return make_response(jsonify(result))
        return wrapper
    return jsend_decorator


class Api_Resource(Resource):

    def prep_json(self, data, status='success', message=None):
            if message is not None:
                result = dict(data=data, status=status, message=message)
            else:
                result = dict(data=data, status=status)
            return result

    def options(self, *args, **kwargs):
        pass

    # method_decorators = [jsend]
