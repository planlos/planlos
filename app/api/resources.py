from flask.ext.restful import Resource
from functools import wraps
from flask import make_response, jsonify
from flask import request

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prep_json(self, data, status='success', message=None):
            if message is not None:
                result = dict(data=data, status=status, message=message)
            else:
                result = dict(data=data, status=status)
            if status != 'success':
                return result, 400
            return result

    def _validate(self, schema=None):
        if schema is None:
            schema = self.schema

        data, errors = schema.load(request.get_json())
        if len(errors):
            return self.prep_json(errors, status='error', message=errors)
        print("DEBUG: validate")
        errors = self.single_schema.validate(data)
        if errors:
            return self.prep_json(errors, status='fail')
        e = locations.create(**data)
        print(e)
        location = self.single_schema.dump(e)
        return self.prep_json(location.data)


    def options(self, *args, **kwargs):
        pass

    # method_decorators = [jsend]
