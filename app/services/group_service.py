from . import Service

# from ..models import User
from ..models.group import Group


class Group_Exists(Exception):
    pass


class No_Such_Group(Exception):
    pass


class Group_Service(Service):
    __model__ = Group

    def all_groups(self):
        return Group.query.all()
