# coding: utf-8

from flask import jsonify, request, redirect, url_for
from ..services import locations
from .resources import Api_Resource
from .schemas import Location_Schema
#from .core import log
import logging as log
import json

from flask.ext.restful import reqparse


class Location_List_Api(Api_Resource):
    def __init__(self, *args, **kwargs):
        self.schema = Location_Schema(many=True)
        self.single_schema = Location_Schema(exclude=['modified_at'])
        super().__init__(*args, **kwargs)

    def get(self):
        r = locations.all()
        log.info(self.schema.dump(r).data)
        result = self.schema.dump(r)
        return self.prep_json({'locations': result.data})

    def post(self):
        data, errors = self.single_schema.load(request.get_json())
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


class Location_Api(Api_Resource):
    def __init__(self, *args, **kwargs):
        self.schema=Location_Schema()
        self.load_schema=Location_Schema(exclude=['modified_at'])
        super().__init__(*args, **kwargs)

    def get(self, id):
        location = locations.get_or_404(id)
        result = self.schema.dump(location)
        return self.prep_json(result.data)

    def post(self, id):
        # Schemas Validation
        json_request = request.data.decode("utf-8")
        data, errors = self.load_schema.loads(json_request)
        location = locations.get_or_404(id)
        if len(errors):
            return self.prep_json(errors, status='error', message=errors)
        print("DEBUG: validate")
        errors = self.load_schema.validate(data)
        if errors:
            return self.prep_json(errors, status='fail')
        e = locations.update(location, **data)
        # return redirect(url_for(Location_Api.get, id=e.id))
        result = self.schema.dump(e)
        return self.prep_json(result.data)
