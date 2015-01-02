from flask import Flask
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security
from flask.ext.babel import Babel
from flask.ext.assets import Environment
from .datastore import Planlos_User_Datastore

mail = Mail()
db = SQLAlchemy()
security = Security()
assets = Environment()
babel = Babel()
user_datastore = Planlos_User_Datastore()
