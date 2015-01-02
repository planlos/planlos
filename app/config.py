# coding: utf-8

# import flask.ext.uploads
import os.path
_basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    SITEURL = 'https://planlosbremen.de'
    # PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = "nnuunnneenrrenereslakfjewrlkjasflflkjsdwerowqierh50175c98ß43czmgr9u,hd497t"
    SESSION_COOKIE_NAME = "c_planlos"
    # PERMANENT_SESSION_LIFETIME = # datetime.timedelta
    # USE_X_SENDFILE = True
    LOGGER_NAME = 'planlos-app'
    # SERVER_NAME = # for subdomains
    # MAX_CONTENT_LENGTH = # in bytes

    # Application Variables
    # GENDER_CHOICES = GENDER_CHOICES
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'planlos.db')
    # File uploads with flask-uploads
    UPLOADED_FLYERS_DEST = 'app/static/uploads/flyers/'
    UPLOADED_FLYERS_URL = '/static/uploads/flyers/'
    # UPLOADED_FLYERS_ALLOW = flask.ext.uploads.IMAGES
    # UPLOADED_FILES_DENY = flask.ext.uploads.DEFAULTS
    UPLOADS_DEFAULT_DEST = 'static/uploads'
    # UPLOADS_DEFAULT_URL

    # File uploads with flask-uploads
    UPLOADED_PHOTO_DEST = 'app/static/uploads/flyers/'
    UPLOADED_PHOTO_URL = '/static/uploads/flyers/'
    # UPLOADED_PHOTO_ALLOW = flask.ext.uploads.IMAGES

    W_SCALE_SIZES = [50, 100, 200, 450, 800, 1024]
    H_SCALE_SIZES = [50, 100, 200]
    BABEL_DEFAULT_LOCALE = 'de_DE.UTF-8'
    BABEL_DEFAULT_TIMEZONE = "Europe/Berlin"

    # planlos database for import
    PLANLOS_DB = 'planlos_db'
    PLANLOS_USER = 'planlos'
    PLANLOS_PASS = 'd7JWXwSqqcUw'
    PLANLOS_HOST = '127.0.0.1'


    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'planlos_dev.db')
    SITEURL = 'http://localhost:5000'


class Testing(Config):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = False
    SITEURL = 'http://localhost:5000'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/planlos_test.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
