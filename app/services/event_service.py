from . import Service

from ..models.events import Event, Event_Cache, Tag
from sqlalchemy import or_
from flask import abort
from datetime import datetime
from werkzeug.exceptions import Unauthorized
from flask.ext.security.core import current_user
from app import db


from dateutil import parser

class Event_Service(Service):
    __model__ = Event

    # override methods for event_cache
    def save(self, model):
        self._isinstance(model)
        model.modified_at = datetime.now()
        Event_Cache.update(model)
        db.session.add(model)
        db.session.commit()
        return model

    def delete(self, model):
        Event_Cache.delete(model)
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()

    def delete_all(self):
        Event.query.delete()
        Event_Cache.query.delete()
        db.session.commit()

    def get_regular(self, day=datetime.today() ):
        start_of_day = datetime(year=day.year,month=day.month, day=day.day, hour=0, minute=0)
        end_of_day = datetime(year=end.year,month=end.month, day=end.day, hour=23, minute=59)
        cached_entries = Event_Cache.query.filter(Event.is_pub==True,
                                                  Event.rrule!=None,
                                                  Event_Cache.date >= start_of_day,
                                                  Event_Cache.date <= end_of_day).order_by(Event_Cache.date).all()
        entries = [entry.event for entry in cached_entries]
        return entries

    def _preprocess_params(self, kwargs):
        kwargs.pop('csrf_token', None)
        if kwargs.get('is_pub'):
            kwargs.pop('is_pub', None)
        kwargs.pop('likes', None)
        kwargs.pop('modified_at', None)
        if kwargs.get('location'):
            print("lOCATION", kwargs['location'])
            kwargs['location_id'] = kwargs['location']['id']
        kwargs.pop('location', None)
        #
        if type(kwargs['dtstart']) is str:
            kwargs['dtstart'] = parser.parse(kwargs['dtstart'])
        if kwargs.get('dtend') and type(kwargs['dtend']) is str:
            kwargs['dtend'] = parser.parse(kwargs['dtend'])

        return kwargs

    def get_by_date(self, day, end=None):
        start_of_day = datetime(year=day.year,month=day.month, day=day.day, hour=0, minute=0)
        if end is None:
            end = day
        end_of_day = datetime(year=end.year,month=end.month, day=end.day, hour=23, minute=59)
        cached_entries = []
        if not current_user.is_anonymous():
            cached_entries = Event_Cache.query.filter(or_(Event.is_pub==True,Event.owner==current_user),
                                                      Event_Cache.date >= start_of_day,
                                                      Event_Cache.date <= end_of_day).order_by(Event_Cache.date).all()
        else:
            cached_entries = Event_Cache.query.filter(Event.is_pub==True,
                                                      Event_Cache.date >= start_of_day,
                                                      Event_Cache.date <= end_of_day).order_by(Event_Cache.date).all()
        entries = [entry.event for entry in cached_entries]
        return entries

    def get_by_tag(self, tags, slice=None):
        if isinstance(tags, str):
            tags = [tag.lower() for tag in tags.split(',')]
        if slice is None:
            events = self.__model__.query.filter(Event.tags.any(Tag.name.in_(tags))).all().order_by(Event.dtstart)
        elif slice == 1:
            events = self.__model__.query.filter(Event.tags.any(Tag.name.in_(tags))).order_by(Event.dtstart).first()
        else:
            events = self.__model__.query.filter(Event.tags.any(Tag.name.in_(tags))).order_by(Event.dtstart).limit(slice)
        return events

    def get_unpublished(self):
        return self.__model__.query.filter(Event.is_pub==False).all()  # order_by(Event.dtstart)

    def get_or_404(self, id):
        entry = super(Event_Service, self).get_or_404(id)
        if not (entry.is_pub or entry.owner == current_user):
            abort(404)
        return entry

    def _isallowed(self, model):
        # if current_user != model.owner or current_user.is_admin():
        #    raise Unauthorized()
        pass

    def update(self, model, **kwargs):
        print(("Update:", kwargs))
        self._isinstance(model)
        # self._isallowed(model)
        for k, v in list(self._preprocess_params(kwargs).items()):
            setattr(model, k, v)
        model = self.save(model)
        return model
