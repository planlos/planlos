# coding: utf-8

from flask import jsonify, request, redirect, url_for
from ..services import locations
from .resources import Api_Resource
from .core import marshmallow
from marshmallow import fields
#from .core import log
import logging as log
import json

class Location_Schema(marshmallow.Schema):
    name = fields.String(required=True)
    email_contact = fields.Email()
    id = fields.Integer()
    postal_code = fields.Number()
    url = fields.Url()
    # modified_at = fields.LocalDateTime()

    class Meta:
        skip_missing = True
        # exclude = ['modified_at']
        fields = ('name',
                  'shortdesc',
                  'street_address',
                  'locality',
                  'region',
                  'postal_code',
                  'country_name',
                  'email_contact',
                  'openinghours',
                  'tel',
                  'fax',
                  'url',
                  'tags',
                  'longitude',
                  'latitude',
                  'modified_at',
                  'id')


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
        # Schemas Validation
        json_request = request.data.decode("utf-8")
        data, errors = self.single_schema.loads(json_request)
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
