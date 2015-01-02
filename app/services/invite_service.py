from ..core import Service
from .invite import Invites
from .user_service import User_Service

class Invalid_Code(Exception):
    pass

class Same_Owner(Exception):
    pass


class Invite_Service(Service):
    __model__ = Invites

    def _check_invite(self, code1, code2):
        invite1 = self.__model__.get(code1)
        invite2 = self.__model__.get(code2)
        if invite1 is None or invite2 is None:
            raise Invalid_Code()
        if invite1.owner == invite2.owner:
            raise Same_Owner()
        return (invite1, invite2)

    def signup_user(user, email, password, code1, code2):
        # may all throw...
        self._check_invite(code1, code2)
        password = users._hash_password(password)
        users = User_Service()
        users.create(username=user, email=email,password=password)
