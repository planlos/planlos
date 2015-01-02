# coding: utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from ..core import db
import uuid

class Invites(db.Model):
    __tablename__ = 'invites'

    code = db.Column(db.Unicode(6), primary_key=True)
    owner = db.Column(db.Integer())

    def __init__(self, uid=None):
        self.owner = uid
        self.code = str(uuid.uuid4())[:6]

    def __repr__(self):
        return "%s:%s" % (self.code, str(self.owner) )

