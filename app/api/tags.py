# coding: utf-8

from ..services import events
from ..services import users
from ..services import locations as locations
from ..models.events import Tag
from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from flask.ext.restful import reqparse
from flask.ext.restful.types import *

from .mappings import *

from datetime import datetime
import dateutil


class Tags_Api(restful.Resource):
    def __init__(self):
        super(Tags_Api, self).__init__()

    @marshal_with(tag_list)
    def get(self):
        reqargs = reqparse.RequestParser()
        reqargs.add_argument('query', type = str)
        args = reqargs.parse_args()
        args = { k:v for k,v in list(args.items()) if v is not None}
        if 'query' in args:
            return {'tags': Tag.query.filter(Tag.name.startswith(args['query'])) }
        else:
            return {'tags': Tag.query.all() }

    @marshal_with(tag_list)
    def post(self):
        reqargs = reqparse.RequestParser()
        reqargs.add_argument('name', type = str, required=True)
        args = reqargs.parse_args()
        args = { k:v for k,v in list(args.items()) if v is not None}
        tag = Tag(name=args['name'])
        return {'tags': tag} , 200


    def delete(self, id):
        e = event_service.get_or_404(id)
        event_service.delete(e)
        return {'deleted': id}
