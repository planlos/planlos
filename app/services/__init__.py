# -*- coding: utf-8 -*-

from app import user_datastore


class Service(object):
    __model__ = None

    def set_db_session(self, session):
        self.session = session

    def _isinstance(self, model, raise_error=True):
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        kwargs.pop('csrf_token', None)
        return kwargs

    def _obey_permissions(self, obey=False, **args):
        pass

    def save(self, model):
        self._isinstance(model)
        self.session.add(model)
        self.session.commit()
        return model

    def all(self):
        return self.__model__.query.all()

    def get(self, id):
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        return self.__model__.query.filter_by(**kwargs)

    def first(self, **kwargs):
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        self._isinstance(model)
        for k, v in list(self._preprocess_params(kwargs).items()):
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        self._isinstance(model)
        self.session.delete(model)
        self.session.commit()

from .event_service import Event_Service
from .flyer_service import Flyer_Service
from .location_service import Location_Service
from .user_service import User_Service
from .group_service import Group_Service


events = Event_Service()
flyers = Flyer_Service()
locations = Location_Service()
users = User_Service(user_datastore)
groups = Group_Service()
