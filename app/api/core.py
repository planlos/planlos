# coding: utf-8

from flask.ext.marshmallow import Marshmallow
from flask.ext.cors import CORS

import logging

marshmallow = Marshmallow()
cors = CORS()
log = logging.getLogger()
