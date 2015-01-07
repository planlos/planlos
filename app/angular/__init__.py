# coding: utf-8
from .. import factory
from .angular import mod as angular


def create_app(settings_override=None):
    app = factory.create_app(__name__, '/',
                             settings_override,
                             static_path='/',
                             static_folder='static')
    app.register_blueprint(angular)
    return app
