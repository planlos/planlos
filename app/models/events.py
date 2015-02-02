# coding: utf-8
from app import db
from datetime import datetime
from .flyer import Flyer
from flask import json


class Event_Cache(db.Model):
    __tablename__ = 'eventcache'

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    eventid = db.Column(db.Integer(), db.ForeignKey('events.id'))
    event = db.relationship('Event', backref='eventcache')

    def __init__(self, date=None, event=None):
        self.date = date
        self.event = event

    def __repr__(self):
        return "{eventid} => {date}".format(eventid=self.event.id, date=self.date.ctime())

    @classmethod
    def update(cls, event):
        Event_Cache.delete(event)
        if event.rrule:
            for event_date in list(event.rrule):
                ec = Event_Cache(event_date, event)
                db.session.add(ec)
                db.session.commit()
        else:
            ec = Event_Cache(event.dtstart, event)
            db.session.add(ec)
            db.session.commit()
        print("Cache updated")

    @classmethod
    def delete(cls, event):
        for event in Event_Cache.query.filter(Event_Cache.eventid == event.id).all():
            print(("Eventcache: ", event))
            # session.delete(event)
            # session.commit()


tagrefs = db.Table('tagrefs',
                   db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                   db.Column('event_id', db.Integer, db.ForeignKey('events.id')))

flyerrefs = db.Table('flyerrefs',
                     db.Column('flyer_id', db.Integer, db.ForeignKey('flyers.id')),
                     db.Column('event_id', db.Integer, db.ForeignKey('events.id')))


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100))

    def __init__(self, name=''):
        try:
            str(name)
        except:
            name = name.encode('latin-1').decode('utf-8', 'ignore')
        self.name = name

    def __unicode__(self):
        return self.name


class Event(db.Model):
    __tablename__ = 'events'

    def __init__(self, **kwargs):
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        super(Event, self).__init__(**kwargs)


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(200))
    subtitle = db.Column(db.Unicode(200))
    desc = db.Column(db.Unicode())
    is_pub = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())

    likes = db.Column(db.Integer(), default=0)

    location_id = db.Column(db.Integer(), db.ForeignKey('locations.id'))
    location = db.relationship('Location', backref='events')


    tags = db.relationship('Tag', secondary=tagrefs,
                           cascade='all',
                           backref=db.backref('events', lazy='dynamic'))
    # mediafiles
    flyers = db.relationship('Flyer', secondary=flyerrefs,
                             cascade='all',
                             backref=db.backref('events', lazy='dynamic'))

    # gender


    # if dtstart and dtend are None then rrule is used
    # date (start)
    # time (start)
    dtstart = db.Column('dtstart', db.DateTime(timezone=True),  nullable=True)
    # time (end) (datetime)
    dtend = db.Column('dtend', db.Time(),  nullable=True, default=None)

    # rrule
    # altogether in a python.dateutil.rrule (or rruleset?)
    rrule = db.Column('rrule', db.PickleType(), default=None, nullable=True)

    # tags
    #tags = Column(Unicode(120), default=None, nullable=True)
    # owner
    owner_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    owner = db.relationship('User', backref='events')

    # comments
    # attendees

    @property
    def day(self):
        return self.dtstart.date()

    def add_tags_by_name(self, taglist):
        for tagname in taglist:
            self.add_tag_by_name(tagname)

    def add_tag_by_name(self, tagname):
        tagname = tagname.lower()
        tag = Tag.query.filter(Tag.name==tagname).first()
        if tag is None:
            tag = Tag(name=tagname)
        if not tag in self.tags:
            self.tags.append(tag)

    def print_rrule(self):
        import pprint
        import sys
        sys.displayhook = pprint.pprint
        if self.rrule is not None:
            print((list(self.rrule)))
            return str(self.rrule.__dict__) + "<br/>"+str(list(self.rrule))
        else:
            return ""
