# coding: utf-8

from ..services import events as eventservice
from ..services import users
from ..services import locations as locations
from ..services import flyers

from ..models.events import Event, Tag
from ..models.flyer import Flyer

from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from ..services.user_service import No_Such_User
import datetime
from flask.ext.restful.utils import cors
from flask.ext.restful import reqparse, marshal


import requests
import json
import sys
import datetime
from dateutil.parser import *

from .resources import Api_Resource

from datetime import datetime
import dateutil


class Flyer_List_Api(Api_Resource):

    def get(self):
        # flyer = flyers.all()
        return {'msg': 'Please help me!'}

    def post(self):
        pass


class Flyer_Api(Api_Resource):
    pass
