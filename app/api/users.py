# coding: utf-8

from ..services import events,users
from ..services import locations as locations

from flask import abort, current_app, request
from flask.ext.login import login_user, logout_user, login_required, current_user
from ..services.user_service import No_Such_User
from flask.ext.restful import reqparse
from flask.ext import restful
from .resources import Api_Resource

class User_List_Api(Api_Resource):

    def get(self):
        rv = [{'uid': u.username, 'email': u.email} for u in users.all()]
        return {'users': rv }


class Auth_Api(Api_Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('logout', type = bool)
        self.reqparse.add_argument('username', type = str)
        self.reqparse.add_argument('password', type = str)
        self.reqparse.add_argument('remember', type = bool)
        super(Auth_Api, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        print(("ARGS:", args))
        if not (args['logout'] is None):
            users.logout() 
        if current_user.is_anonymous():
            return {'current_user': 'Anonymous'}
        else:
            return {'current_user': current_user.username }

    def post(self):
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']
        remember = args['remember']
        print(("Credential: ", (username, password, remember)))
        try:
            users.login(username, password, remember)
            return {'current_user': current_user.username }
        except Exception as e:
            print(e)
            return restful.abort(401)


