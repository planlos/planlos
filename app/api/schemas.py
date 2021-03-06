# coding: utf-8

from .core import marshmallow as ma
from flask import Markup
from dateutil import parser
from dateutil.rrule import *
from marshmallow import ValidationError, fields


class Location_Schema(ma.Schema):
    id = ma.Integer()
    name = ma.String(required=True)
    email_contact = ma.Email()
    postal_code = ma.Integer(as_string=True)
    url = ma.Url()

    class Meta:
        skip_missing = True
        exclude = ['created_at', 'is_pub', 'photos', 'tags']
        fields = ('name', 'postal_code', 'id', 'shortdesc', 'desc', 'street_address', 'locality', 'region',
                  'country_name', 'email_contact', 'openinghours', 'tel',
                  'fax', 'url', 'longitude', 'latitude', 'modified_at')


class Tag_Schema(ma.Schema):
    class Meta:
        fields = ['name']



def must_be_rrule_freq_word(data):
    freq = ['MONTHLY', 'WEEKLY', 'DAILY', 'HOURLY']
    if data not in freq:
        raise ValidationError('freq must be in {}'.format(freq))


def mapfreq(obj):
    if type(obj) is str:
        must_be_rrule_freq_word(obj)
        freq = {'MONTHLY': MONTHLY,
                'WEEKLY': WEEKLY,
                'DAILY': DAILY,
                'HOURLY': HOURLY}
        return freq[obj]


class RRule_Schema(ma.Schema):
    def parse_date(self, obj):
        return obj.isoformat()

    def deserialize_date(self, value):
        return parser.parse(value)

    dtstart = ma.Method("parse_date", "deserialize_date", required=True)
    freq = ma.String(required=True, validate=must_be_rrule_freq_word)

    interval = ma.Integer(default=1)
    count = ma.Integer()
    until = ma.Method("parse_date", "deserialize_date")
    bysetpos = ma.Integer()  # Sould be a list for rrule
    bymonth = ma.Integer()
    bymonthday = ma.Integer()
    byweekday = ma.Integer()


    def make_object(self, data):
        if data.get('interval') is None:
            interval = 1
        else:
            interval = data.get('interval')
        return rrule(mapfreq(data.get('freq')),
                     dtstart=data.get('dtstart'),
                     until=data.get('until'),
                     interval=interval,
                     count=data.get('count'),
                     bysetpos=data.get('bysetpos'),
                     bymonth=data.get('bymonth'),
                     bymonthday=data.get('bymonthday'),
                     byweekday=data.get('byweekday'),
                     )


class RRule_Field(fields.Field):
    def _serialize(self, value, attr, obj):
        if attr == 'rrule':
            retval = dict()
            for key, value in value.__dict__.items():
                if value is None:
                    continue
                if key not in ['_freq', '_until', '_byweekday', '_dtstart', '_bysetpos', '_bymonth', '_count', '_bymonthday']:
                    continue
                if key == '_dtstart':
                    value = value.isoformat()
                retval.update({key[1:]: value})
            return retval

    def _deserialize(self, data):
        if data.get('interval') is None:
            interval = 1
        else:
            interval = data.get('interval')
        return rrule(mapfreq(data.get('freq')),
                     dtstart=parser.parse(data.get('dtstart')),
                     until=data.get('until'),
                     interval=interval,
                     count=data.get('count'),
                     bysetpos=data.get('bysetpos'),
                     bymonth=data.get('bymonth'),
                     bymonthday=data.get('bymonthday'),
                     byweekday=data.get('byweekday'),
                    )

@RRule_Schema.preprocessor
def create_fields(schema, in_data):
    if 'rrule' in in_data:
        rr = in_data['rrule']
        in_data['dtstart'] = rr.dtstart
        in_data['freq'] = rr.freq
        in_data['interval'] = rr.interval
        in_data['count'] = rr.count
        in_data['until'] = rr.until
        del in_data['rrule']
    return in_data


def rrule_validator(obj):
    if type(obj) == rrule:
        return True
    else:
        return False


class Event_Schema(ma.Schema):

    def parse_date(self, obj):
        return obj.isoformat()

    def deserialize_date(self, value):
        return parser.parse(value)

    id = ma.Integer()
    title = ma.String(required=True)
    location = ma.Nested(Location_Schema)
    tags = ma.Nested(Tag_Schema, many=True)
    #dtstart = ma.Method("parse_date", "deserialize_date", required=True)
    dtstart = ma.DateTime(required=True)
    #rrule = ma.Nested(RRule_Schema, default = None)
    rrule = RRule_Field()

    class Meta:
        skip_missing = True
        exclude = ['is_pub', 'created_at', 'flyers', 'owner', 'owner_id']
        additional = ('subtitle', 'desc', 'location_id', 'location', 'rrule', 'dtstart')


@Location_Schema.preprocessor
@Event_Schema.preprocessor
def remove_modified(schema, in_data):
    if in_data.get('modified_at') is not None:
        del in_data['modified_at']
    return in_data


@Event_Schema.preprocessor
def create_location_id(schema, data):
    print(data)
    data['location_id'] = data['location']['id']
    return data


@Event_Schema.validator
def validate_title(schema, data):
    # get title
    title = data['title']
    title = Markup(title).striptags()
    for c in ";`´\n\t\r":
        title = title.replace(c, '')
    # store title again
    data['title'] = title
    return data
