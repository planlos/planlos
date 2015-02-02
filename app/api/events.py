# coding: utf-8

from flask import request

from ..services import events as event_service
from .resources import Api_Resource
from .core import marshmallow
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse

import json
from .schemas import Event_Schema


class Events_by_Day(Api_Resource):
    def get(self, year, month, day):
        date = datetime(year=year, month=month, day=day, hour=0, minute=0)
        result = Event_Schema(many=True).dump(event_service.get_by_date(date))
        return self.prep_json({'events': result.data})


class Events_by_Month(Api_Resource):
    def get(self, year, month):
        date = datetime(year=year, month=month, day=1, hour=0, minute=0)
        date2 = date+timedelta(days=31)
        result = Event_Schema(many=True).dump(event_service.get_by_date(date, date2))
        return self.prep_json({'events': result.data})


class Event_List_Api(Api_Resource):
    def __init__(self):
        self.load_schema = Event_Schema(exclude='modified_at')
        self.single_schema = Event_Schema()
        super(Event_List_Api, self).__init__()

    def get(self):
        result = Event_Schema(many=True).dump(event_service.get_by_date(datetime.now()))
        return self.prep_json({'events': result.data})

    def post(self):
        print("DEBUG: post")
        # Schemas Validation
        json_request = request.data.decode("utf-8")
        data, errors = self.load_schema.loads(json_request)
        if len(errors):
            return self.prep_json(errors, status='error', message=errors)
        #print("DEBUG: validate")
        #errors = self.load_schema.validate(data)
        #if errors:
        #    return self.prep_json(errors, status='fail')
        e = event_service.create(**data)
        print ("API: ", e.rrule )
        result = Event_Schema().dump(e)
        return self.prep_json({'events': result.data})



class Event_Api(Api_Resource):
    def __init__(self):
        self.load_schema = Event_Schema(exclude=['modified_at'])
        self.schema = Event_Schema()

    def get(self, id):
        result = self.load_schema.dump(event_service.get_or_404(id))
        return self.prep_json(result.data)

    def post(self, id):
        print("DEBUG: post")
        # Schemas Validation
        json_request = request.data.decode("utf-8")
        data, errors = self.load_schema.loads(json_request)
        event = event_service.get_or_404(id)
        if len(errors):
            return self.prep_json(errors, status='error', message=errors)
        e = event_service.update(event, **data)
        result = self.schema.dump(e)
        return self.prep_json(result.data)

    def delete(self, id):
        e = event_service.get_or_404(id)
        event_service.delete(e)
        return prep_json({'deleted': id})
