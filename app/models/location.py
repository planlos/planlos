# coding: utf-8

from app import db
from sqlalchemy import Column, Integer, Unicode, Table, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, backref
from datetime import datetime


photorefs = db.Table('photorefs',
                  db.Column('photo_id', db.Integer, db.ForeignKey('photos.id')),
                  db.Column('location_id', db.Integer, db.ForeignKey('locations.id')))


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer(), primary_key=True)
    uploaded_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())
    # owner_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    # owner = db.relationship('User', backref='users')
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'))
    filename= db.Column(db.Unicode(200))
    origfilename= db.Column(db.Unicode(200))
    comment = db.Column(db.Unicode(200))
    sizes = db.Column(db.Unicode(100))

    def __init__(self, filename='', user=None):
        self.owner = user
        self.filename = filename  # self.make_hash(filename)
        self.origfilename = filename
        self.uploaded_at = datetime.now()
        self.modified_at = datetime.now()
        self.comment = ''

    def url(self, size='o'):
        size_path = ''
        #return app.config['UPLOADED_PHOTO_URL']+'/'+size_path+'/'+self.filename


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(200), unique=True)
    shortdesc = db.Column(db.Unicode())
    desc = db.Column(db.Unicode())
    street_address = db.Column(db.Unicode())
    locality = db.Column(db.Unicode())
    region = db.Column(db.Unicode())
    postal_code = db.Column(db.Unicode())
    country_name = db.Column(db.Unicode())
    email_contact = db.Column(db.Unicode())
    openinghours = db.Column(db.Unicode())
    tel = db.Column(db.Unicode())
    fax = db.Column(db.Unicode())
    url = db.Column(db.Unicode())
    tags = db.Column(db.Unicode())
    longitude = db.Column(db.Float())
    latitude = db.Column(db.Float())
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())
    is_pub = db.Column(db.Boolean())
    photos = db.relationship('Photo', secondary=photorefs,
                             cascade='all',
                             backref=db.backref('locations', lazy='dynamic'))

    def __init__(self, **kwargs):
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        super(Location, self).__init__(**kwargs)

    def __unicode__(self):
        return self.name
