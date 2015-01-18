# coding: utf-8

from flask.ext.restful import fields

from datetime import datetime
import dateutil

class TagItem(fields.Raw):
    def format(self, value):
        return value.name

tag_fields = {
    'name': fields.String,
    'id': fields.Integer
}

tag_list = {
    'tags': fields.Nested(tag_fields)
}

flyer_fields = {
    'id': fields.Integer,
}

location_short = {
    'id': fields.Integer,
    'name': fields.String,
    'shortdesc': fields.String,
    'url': fields.String,
    'uri': fields.Url("location", absolute=True),
}

location_full = {
    'id': fields.Integer,
    'name': fields.String,
    'street_address': fields.String,
    'locality': fields.String,
    'region': fields.String,
    'postal_code': fields.String,
    'country_name': fields.String,
    'openinghours': fields.String,
    'tel': fields.String,
    'fax': fields.String,
    'shortdesc': fields.String,
    'desc': fields.String,
    'url': fields.String,
    'email_contact': fields.String,
    # 'tags': fields.List(TagItem()),
    'tags': fields.String,
    'longitude': fields.String,
    'latitude': fields.String,
    'uri': fields.Url('location')
}

location_resource = {
    'location': fields.Nested(location_full)
}

location_list = {
    'locations': fields.Nested(location_resource)
}

user_resource = {
    'username': fields.String,
    'displayname': fields.String,
    'id': fields.Integer,
    'uri': fields.Url("users", absolute=True)
}


event_fields = {
    'id': fields.Integer,
    'title':   fields.String,
    'subtitle': fields.String,
    'desc': fields.String,
    'tags': fields.List(TagItem()),
    # 'tags': fields.String,
    'dtstart': fields.DateTime(default=None),
    'location': fields.Nested(location_short),
    'dtend': fields.DateTime(default=None),
    'is_pub': fields.Boolean,
    'rrule': fields.String,
    # 'owner': fields.Nested(user_resource),
}

event_list = {
    'events': fields.Nested(event_fields)
}


# parse with dateutil
def parseddate(date):
    if date is None:
        return date
    else:
        return dateutil.parser.parse(date)
