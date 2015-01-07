# coding: utf-8

from ..services import events as event_service
from ..services import users
from ..services import locations as locations

from flask import current_app
from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from ..services.user_service import No_Such_User
import datetime
from flask.ext.restful.utils import cors
from flask.ext.restful import reqparse

from .mappings import *

from datetime import datetime
import dateutil
from dateutil.parser import parse

class Event_List_Api(restful.Resource):
    def __init__(self):
        super(Event_List_Api, self).__init__()
        #v = self.as_view('event_list_api')
        #current_app.add_url_rule('/api/events/<int:year>/<int:month>/<int:day>', view_func=event_list_api)

    @marshal_with(event_list)
    def get(self):
        reqargs = reqparse.RequestParser()
        reqargs.add_argument('daterange', type = str)
        reqargs.add_argument('day', type = int)
        reqargs.add_argument('month', type = str)
        args = reqargs.parse_args()
        if args['day'] is not None:
            return {'events': event_service.get_by_date(parse(str(args['day'])))}
        if args['month'] is not None:
            month = args['month']
            date = datetime(year=int(month[0:4]), month=int(month[4:6]), day=1,hour=0, minute=0 )
            date2 = date+timedelta(days=31)
            print(("from ", date, " to ", date2))
            return {'events': event_service.get_by_date(date, date2)}
        return {'events': event_service.get_by_date(datetime.now())}


    @marshal_with(event_list)
    def post(self):
        reqargs = reqparse.RequestParser()
        reqargs.add_argument('title', type = str, required=True)
        reqargs.add_argument('subtitle', type = str)
        reqargs.add_argument('desc', type = str)
        reqargs.add_argument('is_pub', type = bool)
        reqargs.add_argument('likes', type = int)
        reqargs.add_argument('location_id', type = int)
        reqargs.add_argument('tags', type = list)
        reqargs.add_argument('flyers', type = list)
        reqargs.add_argument('dtstart', type = parseddate, required=True)
        reqargs.add_argument('dtend', type = parseddate)
        reqargs.add_argument('rrule', type = str)
        args = reqargs.parse_args()
        args = { k:v for k,v in list(args.items()) if v is not None}
        e = event_service.create(**args)
        return {'event': e} , 200


class Event_Api(restful.Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str)
        self.reqparse.add_argument('subtitle', type = str)
        self.reqparse.add_argument('desc', type = str)
        self.reqparse.add_argument('is_pub', type = bool)
        self.reqparse.add_argument('likes', type = int)
        self.reqparse.add_argument('location_id', type = int)
        self.reqparse.add_argument('tags', type = list)
        self.reqparse.add_argument('flyers', type = list)
        self.reqparse.add_argument('dtstart', type = parseddate)
        self.reqparse.add_argument('dtend', type = parseddate)
        self.reqparse.add_argument('rrule', type = str)
        super(Event_Api, self).__init__()

    @marshal_with(event_fields)
    def get(self,id):
        return event_service.get_or_404(id)

    def post(self, id):
        return self.patch(id)

    def options (self):
        return {'Allow' : 'PUT' }, 200, { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : 'PUT,GET' }


    
    @marshal_with(event_fields)
    def patch(self, id):
        e = event_service.get_or_404(id)
        args = self.reqparse.parse_args()
        args = { k:v for k,v in list(args.items()) if v is not None}
        e = event_service.update(e, **args)
        return {'event': e} , 201

    def delete(self, id):
        e = event_service.get_or_404(id)
        event_service.delete(e)
        return {'deleted': id}
