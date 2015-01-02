
from flask.ext.security import UserMixin, RoleMixin
from datetime import datetime
from .. import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.Unicode(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.Unicode(256))
    registered_at = db.Column(db.DateTime())
    confirmed_at = db.Column(db.DateTime())
    last_login = db.Column(db.DateTime())
    last_modified = db.Column(db.DateTime())
    active = db.Column(db.Boolean(), default=False)
    displayname = db.Column(db.Unicode(80))
    jabber = db.Column(db.String(80))

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        self.registered_at = kwargs.pop('registered_at', datetime.now())
        self.modified_at = kwargs.pop('modified_at', datetime.now())
        self.last_login = kwargs.pop('last_login', datetime.now())
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return "<User(username='%s', email='%s', password='%s')>" % (self.username, self.email, self.password)

    def save(self):
        self.last_modified = datetime.now()
        db.session.add(self)
        db.session.commit()


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
