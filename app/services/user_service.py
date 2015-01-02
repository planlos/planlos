from . import Service

from ..models import User, Role
from ..models.group import Group
from flask import current_app
from flask.ext.security import login_user, logout_user, login_required, current_user
from flask.ext.security.datastore import UserDatastore
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_changed
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash


class User_Exists(Exception):
    pass


class Email_Not_Unique(Exception):
    pass


class No_Such_User(Exception):
    pass


class User_Service(Service):
    __model__ = User

    def __init__(self, user_datastore):
        self.datastore = user_datastore
        super().__init__()

    def _process_pw(self, kwargs):
        if 'password' in kwargs:
            kwargs['password'] = self._hash_password(kwargs['password'])
        return kwargs

    def find(self, **kwargs):
        return self.datastore.find_user(**kwargs)

    def new(self, **kwargs):
        self._process_pw(kwargs)
        return self.__model__(**self._preprocess_params(kwargs))

    def all_groups(self):
        return Group.query.all()

    def logout(self, user=current_user):
        logout_user()
        identity_changed.send(current_app._get_current_object(),
                              identity=AnonymousIdentity())

    def login(self, username, password, remember=False):
        user = self.__model__.query.filter_by(username=username).first()
        if user is None:
            raise No_Such_User("No Such User or Wrong Password")
        # Check password
        if self._check_password(user, password):
            # stamp login_time
            user.last_login = datetime.now()
            login_user(user, remember=remember)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            return self.save(user)
        else:
            raise No_Such_User("No Such User or Wrong Password")

    def _hash_password(self, password):
        return generate_password_hash(password)

    def _django_check_password_hash(self, hashed_pw, pw):
        method, salt, pwhash = hashed_pw.split('$', 2)
        method = method.split(':')[1]
        hash_func = None
        if method == 'sha1':
            hash_func = hashlib.sha1
        elif method == 'md5':
            hash_func = hashlib.md5
        h = hash_func()
        h.update(salt+pw)
        return h.hexdigest() == pwhash

    def _check_password(self, user, password):
        print(("PASS:", user.password))
        if user.password.startswith('django:'):
            return self._django_check_password_hash(user.password, password)
        return check_password_hash(user.password, password)
