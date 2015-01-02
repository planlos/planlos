# coding: utf-8

from ..services import locations
from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from flask.ext.restful.utils import cors
from flask.ext.restful import reqparse

from .mappings import *



class Location_List_Api(restful.Resource):

    @marshal_with(location_list)
    #@cors.crossdomain(origin='*')
    def get(self):
        return { 'locations': locations.all() }

    @marshal_with(location_list)
    def post(self):
        reqargs = reqparse.RequestParser()
        reqargs.add_argument('name', type = str, required=True)
        reqargs.add_argument('shortdesc', type = str)
        reqargs.add_argument('desc', type = str)
        reqargs.add_argument('addr', type = str)
        reqargs.add_argument('email_contact', type = str)
        reqargs.add_argument('url', type = str)
        reqargs.add_argument('tags', type = str)
        reqargs.add_argument('longitude', type = float)
        reqargs.add_argument('latitude', type = float)
        args = reqargs.parse_args()
        args = { k:v for k,v in list(args.items()) if v is not None}
        e = locations.create(**args)
        return {'locations': e} , 200

class Location_Api(restful.Resource):
    def __init__(self):
        self.reqargs = reqparse.RequestParser()
        self.reqargs.add_argument('name', type = str, required=True)
        self.reqargs.add_argument('shortdesc', type = str)
        self.reqargs.add_argument('desc', type = str)
        self.reqargs.add_argument('addr', type = str)
        self.reqargs.add_argument('email_contact', type = str)
        self.reqargs.add_argument('url', type = str)
        self.reqargs.add_argument('tags', type = str)
        self.reqargs.add_argument('longitude', type = float)
        self.reqargs.add_argument('latitude', type = float)

    @marshal_with(location_resource)
    #@cors.crossdomain(origin='*')
    def get(self, id):
        return { 'location': locations.get_or_404(id) }

    def post(self, id):
        return self.patch(id)

    @marshal_with(location_resource)
    def patch(self, id):
        l = locations.get_or_404(id)
        args = self.reqargs.parse_args()
        args = { k:v for k,v in list(args.items()) if v is not None}
        l = locations.update(l, **args)
        return {'location': l} , 201
