# coding: utf-8

from datetime import datetime
from . import Base

from sqlalchemy import Column, Integer, Unicode, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer(), primary_key=True)
    uploaded_at = Column(DateTime())
    modified_at = Column(DateTime())
    #owner_id = Column(Integer(), ForeignKey('users.id'))
    #owner = relationship('User', backref='users')
    owner = Column(Integer(), ForeignKey('users.id'))
    filename= Column(Unicode(200))
    origfilename= Column(Unicode(200))
    comment = Column(Unicode(200))
    sizes = Column(Unicode(100))

    def __init__(self, filename='', user=None):
        self.owner = user
        self.filename = filename #self.make_hash(filename)
        self.origfilename = filename
        self.uploaded_at = datetime.now()
        self.modified_at = datetime.now()
        self.comment = ''

    def url(self, size='o'):
        size_path=''
        return app.config['UPLOADED_PHOTO_URL']+'/'+size_path+'/'+self.filename
