# coding: utf-8

from flask import jsonify
from flask.ext import restful
from flask.ext.restful.utils import cors
from .. import factory
from .events import Event_List_Api, Event_Api, Events_by_Day, Events_by_Month
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
    restapi = restful.Api(app, decorators=[cors.crossdomain(origin='*', methods='*',
                                                            headers='Origin, X-Requested-With, Content-Type, Accept, Options')])
    restapi.add_resource(Tags_Api, '/tags/', endpoint='tags')
    restapi.add_resource(Flyer_List_Api, '/flyers/', endpoint='flyers')
    restapi.add_resource(Flyer_Api, '/flyers/<int:id>', endpoint='flyer')
    restapi.add_resource(Events_by_Day, '/events/<int:year>/<int:month>/<int:day>')
    restapi.add_resource(Events_by_Month, '/events/<int:year>/<int:month>')
    restapi.add_resource(Event_Api, '/event/<int:id>')
    restapi.add_resource(Event_List_Api, '/events/', endpoint='events')
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

    @app.after_request
    def after(response):
        print(response.headers)
        return response


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
