# coding: utf-8

from app import db


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.Unicode(80), unique=True)
    # members = relationship("User",
    #                        secondary=members,
    #                        backref=backref("groups", lazy='dynamic'))

    def __init__(self, groupname):
        self.groupname = groupname

    def __repr__(self):
        return '<Group %r>' % self.groupname
