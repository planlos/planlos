#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from app import frontend
from app import api
from app import angular
from app import db

frontend = frontend.create_app(settings_override="app.config.Development")
angular = angular.create_app(settings_override="app.config.Development")

application = DispatcherMiddleware(frontend, {
    '/api': api.create_app(settings_override="app.config.Development"),
    '/app': angular,
})

if __name__ == "__main__":
    with frontend.app_context():
        db.create_all()
    run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)
