# coding: utf-8

from flask import render_template, abort, jsonify
from flask.ext import restful
from flask.ext.restful.utils import cors
from .. import factory
from .events import Event_List_Api, Event_Api
from .users import User_List_Api
from .users import Auth_Api
from .tools import Tools_Api
from .flyers import Flyer_Api, Flyer_List_Api
from .locations import Location_List_Api, Location_Api
from .tags import Tags_Api


def create_app(settings_override=None):
    app = factory.create_app(__name__, '/api', settings_override)
    # Set the default JSON encoder

    # restapi.init_app(app)
    restapi = restful.Api(app, decorators=[cors.crossdomain(origin='*')])
    restapi.add_resource(Tags_Api, '/tags/', endpoint='tags')
    restapi.add_resource(Flyer_List_Api, '/flyers/', endpoint='flyers')
    restapi.add_resource(Flyer_Api, '/flyers/<int:id>', endpoint='flyer')
    restapi.add_resource(Event_List_Api, '/events/', endpoint='events')
    restapi.add_resource(Event_Api, '/events/<int:year>/<int:month>/<int:day>', endpoint='eventday')
    restapi.add_resource(Event_Api, '/events/<int:year>/<int:month>', endpoint='eventmonth')
    restapi.add_resource(Event_Api, '/events/<int:id>', endpoint='event')
    restapi.add_resource(User_List_Api, '/users/', endpoint='users')
    restapi.add_resource(Auth_Api, '/auth/', endpoint='auth')
    restapi.add_resource(Location_List_Api, '/locations/', endpoint='locations')
    restapi.add_resource(Location_Api, '/locations/<int:id>', endpoint='location')
    restapi.add_resource(Tools_Api, '/tools/', endpoint='tools')

    app.errorhandler(404)(not_found)
    app.errorhandler(403)(forbidden)
    app.errorhandler(401)(unauthorized)

#    @app.route('/')
#    def index():
#        return jsonify(dict(status=200)), 200

    print((app.url_map))
    # app.config['JSON_AS_ASCII'] = False
    print(("JSON CONFIG", app.config['JSON_AS_ASCII']))
    return app


def forbidden(e):
    return jsonify(dict(error=e.msg)), 403


def unauthorized(e):
    return jsonify(dict(error=e.description)), 401


def not_found(e):
    return jsonify(dict(error='Not found')), 404


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
