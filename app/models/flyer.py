# coding: utf-8

from app import db
from datetime import datetime
from flask import json, current_app


class Flyer(db.Model):
    __tablename__ = 'flyers'

    id = db.Column(db.Integer(), primary_key=True)
    uploaded_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())
    owner_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    owner = db.relationship('User', backref='users')
    filename= db.Column(db.Unicode(200))
    origfilename= db.Column(db.Unicode(200))
    comment = db.Column(db.Unicode(200))

    def __init__(self, filename='', user=None):
        self.owner = user
        self.filename = filename #self.make_hash(filename)
        self.origfilename = filename
        self.uploaded_at = datetime.now()
        self.modified_at = datetime.now()
        self.comment = ''

    def serialize(self):
        src = dict( (key, current_app.config['UPLOADED_FLYERS_URL']+"/"+str(key)+"/"+self.filename)
                    for key in current_app.config['W_SCALE_SIZES'])
        return {
            'id': self.id,
            'filename': json.dumps(self.filename),
            'src': src,
        }

    def thumbnail(self):
        return "<img src=\"%s\" class=\"thumbnail\" />" % (current_app.config['UPLOADED_FLYERS_URL']+"/50/"+self.filename)

#    def url(self, size='o'):
#        size_path=''
#        return current_app.config['FLYER_UPLOAD_PATH']+'/'+size_path+'/'+self.filename

