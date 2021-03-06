# coding: utf-8

# from . import permissions
# from .adminaddons import create_admin
# from .assets import create_assets

from flask import Flask, send_from_directory

from . import db, mail, security, babel, user_datastore
from .models import User, Role


def create_app(package_name, package_path, settings_override=None, **kwargs):
    app = Flask(__name__, **kwargs)
    app.config.from_object('app.config.Config')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    mail.init_app(app)
    db.init_app(app)
    babel.init_app(app)
    user_datastore.init(db, User, Role)
    security.init_app(app, user_datastore)

    return app
