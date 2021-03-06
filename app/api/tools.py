# coding: utf-8

from ..services import events as eventservice
from ..services import locations as locations
from ..models.location import Location
from ..models import User
from ..models.events import Tag
from .resources import Api_Resource
from flask.ext.restful import reqparse
import requests

from dateutil.parser import parse

from .. import db

action_types = [
    '',  # there is no primary key with 0
    'Konzert',  # 1
    'Demo',  # 2
    'Party',  # 3
    'Lesung',  # 4
    'Infoveranstaltung',  # 5
    'Kneipe',  # 6
    'Vokü',  # 7
    'Plenum',  # 8
    'Treffen (Gruppe)',  # 9
    'Sonstiges',  # 10
    'Öffnungszeiten',  # 11
    'Film',  # 12
    'Cafe',  # 13
    'Spiel+Spass',  # 14
    'Frühstück',  # 15
    'Vortrag',  # 16
    'Treffen',  # 17
    'Ausstellung',  # 18
    'Seminar',  # 19
    'Workshop',  # 20
    'Kundgebung',  # 21
    'Keinen Meter (1.Mai 2011)',  # 22
]


class Tools_Api(Api_Resource):
    def __init__(self):
        self.cmdmap = {}
        self.cmdmap.update({'import_data': getattr(self, '_import_data')})
        self.cmdmap.update({'delete_all': getattr(self, '_delete_all')})
        super(Tools_Api, self).__init__()

    def get(self):
        return {'msg': 'Please help me!'}

    def post(self):
        reqargs = reqparse.RequestParser()
        reqargs.add_argument('cmd', type=str, required=True)
        args = reqargs.parse_args()
        try:
            if str(args['cmd']) in self.cmdmap:
                self.cmdmap[args['cmd']]()
                return {'msg': 'ok'}, 200
                return {'status': 'command not found'}, 404
        except Exception as e:
            return {'error': e}, 500

    def _import_data(self):
        self._delete_all()
        eventurl="https://planlosbremen.de/termine/service/monat/"
        locationurl="https://planlosbremen.de/termine/service/location/"
        r = requests.get(eventurl, verify=False)
        data = r.json()
        msg = []
        for item in data:
            fields = item['fields']
            e = eventservice.new()
            e.title = fields['title'].encode('latin1').decode('utf-8', 'ignore')
            e.subtitle = fields['short_desc'].encode('latin1').decode('utf-8', 'ignore')
            e.desc = fields['desc'].encode('latin1').decode('utf-8', 'ignore')
            e.is_pub = fields['is_pub']
            e.dtstart = parse('{0} {1}'.format(fields['datum'], fields['time']))
            e.owner = User.query.get(1)
            ## get location
            loc_id = fields['location']
            rloc = requests.get(locationurl+str(loc_id), verify=False)
            locdata = rloc.json()
            lf = locdata[0]['fields']
            location_name = lf['name'].encode('latin1').decode('utf-8', 'ignore')
            l = Location.query.filter(Location.name==location_name).first()
            if not l:
                l = locations.new()
                l.name = location_name
                l.desc = lf['selfportrait'].encode('latin1').decode('utf-8', 'ignore')
                l.url = lf['url']
                l.street_address = lf['address'].encode('latin1').decode('utf-8', 'ignore')
                locations.update(l)
            e.location = l
            tag_name = action_types[int(fields['type'])].lower()
            t = Tag.query.filter(Tag.name==tag_name).first()
            if not t:
                t = Tag(tag_name)
                db.session.add(t)
                db.session.commit()
            e.tags = [t]
            eventservice.update(e)
            msg += 'Event: %s added' % e.title
        return msg

    def _delete_all(self):
        eventservice.delete_all()
        locations.delete_all()
        return "deleted all events"
