# coding: utf-8

from ..services import events
from ..services import users
from ..services import locations as locations
from ..models.events import Tag
from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from flask.ext.restful import reqparse


from .resources import Api_Resource

from datetime import datetime
import dateutil


class Tags_Api(Api_Resource):
    def __init__(self):
        super(Tags_Api, self).__init__()

    def get(self):
        pass

    def post(self):
        pass


