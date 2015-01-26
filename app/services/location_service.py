from . import Service

from ..models.location import Location
from datetime import datetime
from app import db

class Location_Service(Service):
    __model__ = Location

    def get_by_region(self, regiontag):
        return self.__model__.query.filter(Location.tags == regiontag)

    def delete_all(self):
        Location.query.delete()

    def save(self, model):
        self._isinstance(model)
        model.modified_at = datetime.now()
        db.session.add(model)
        db.session.commit()
        return model

    def delete(self, model):
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()

    def _preprocess_params(self, kwargs):
        # delete unused or dangerous fields
        kwargs.pop('csrf_token', None)
        kwargs.pop('likes', None)
        kwargs.pop('modified_at', None)

        # fields deleted that user may not changes
        if kwargs.get('is_pub'):
            kwargs.pop('is_pub', None)

        if kwargs.get('location'):
            kwargs['location_id'] = kwargs['location']['id']
        kwargs.pop('location', None)

        return kwargs

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
