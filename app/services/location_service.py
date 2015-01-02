from . import Service

from ..models.location import Location

class Location_Service(Service):
    __model__ = Location

    def get_by_region(self, regiontag):
        return self.__model__.query.filter(Location.tags == regiontag)

    def delete_all(self):
        Location.query.delete()
        #db.session.commit()
