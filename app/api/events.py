# coding: utf-8

from ..services import events as event_service
from flask import request
from flask.ext.restful import marshal_with
from datetime import datetime
from datetime import timedelta
from flask.ext.restful import reqparse
from .mappings import *
from .resources import Api_Resource
from dateutil.parser import parse
from .parsers import *

class Events_by_Day(Api_Resource):
    @marshal_with(event_list)
    def get(self, year, month, day):
        date = datetime(year=year, month=month, day=day, hour=0, minute=0)
        return {'events': event_service.get_by_date(date)}


class Events_by_Month(Api_Resource):
    @marshal_with(event_list)
    def get(self, year, month):
        date = datetime(year=year, month=month, day=1, hour=0, minute=0)
        date2 = date+timedelta(days=31)
        return {'events': event_service.get_by_date(date, date2)}


class Event_List_Api(Api_Resource):
    def __init__(self):
        super(Event_List_Api, self).__init__()

    @marshal_with(event_list)
    def get(self):
        return {'events': event_service.get_by_date(datetime.now())}


class Event_Api(Api_Resource):
    @marshal_with(event_fields)
    def get(self, id):
        return event_service.get_or_404(id)

    def post(self):
        print("DEBUG: post")
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=parsers.event_title, required=True)
        parser.add_argument('subtitle', type=parsers.event_subtitle)
        parser.add_argument('desc')
        parser.add_argument('rrule', type=rrule_field)
        parser.add_argument('dtstart', type=dtfield, required=True)
        parser.add_argument('dtend', type=dtfield)
        parser.add_argument('location_id', type=int)
        parser.remove_argument('location')
        return e

    @marshal_with(event_fields)
    def patch(self, id):
        print("DEBUG: patch")
        e = event_service.get_or_404(id)
        print("DEBUG: patch1")
        args = self.reqparse.parse_args(request)
        print("DEBUG: patch2")
        args = {k: v for k, v in list(args.items()) if v is not None}
        e = event_service.update(e, **args)
        print("DEBUG: patch3")
        return {'event': e}, 201

    def delete(self, id):
        e = event_service.get_or_404(id)
        event_service.delete(e)
        return {'deleted': id}
