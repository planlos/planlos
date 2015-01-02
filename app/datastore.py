from flask.ext.security.datastore import Datastore, UserDatastore, SQLAlchemyUserDatastore

class Planlos_User_Datastore(Datastore):
    def __init__(self):
        self._initialised = False

    def init(self, db, usermodel, rolemodel):
        self._datastore = SQLAlchemyUserDatastore(db, usermodel, rolemodel)
        self._initialised = True

    def __getattr__(self, name):
        if not self._initialised: raise TypeError
        return getattr(self._datastore, name)
