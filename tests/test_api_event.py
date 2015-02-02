from . import PlanlosApiTest
from app.models import User, Role
from app.models.events import Event
from app.models.events import Event_Cache
from app.models.location import Location
from app import db

import factory
import factory.alchemy
import factory.fuzzy
from nose.tools import nottest
import datetime
import json
from dateutil.parser import parse

class Event_Factory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = db.session

    # id = 1 ## _sequence als kwarg
    id = factory.Sequence(lambda n: n)
    title = factory.fuzzy.FuzzyText(length=20, prefix="Event_")
    subtitle = "kurz"
    desc = "Beschreibung"
    is_pub = True
    dtstart = factory.fuzzy.FuzzyDate(datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(days=365))


class Today_Event_Factory(Event_Factory):
    dtstart = datetime.datetime.now()+datetime.timedelta(seconds=2)


class Test_Event_Api(PlanlosApiTest):
    def setUp(self):
        super().setUp()
        self.myuser = User(username='test', email='test@localhost', password='test')
        self.adminrole = Role(name='admin', description='Admin User')
        self.editorrole = Role(name='editor', description='Editor')
        self.myuser.roles = [self.adminrole]
        db.session.add(self.myuser)
        db.session.add(self.adminrole)
        db.session.add(self.editorrole)
        db.session.commit()

        # factory_boy
        # create_some_events

    def tearDown(self):
        db.drop_all()
        db.session.remove()

    def _create_date(self):
        date = factory.fuzzy.FuzzyNaiveDateTime(datetime.datetime.now(),
                                                datetime.datetime.now()+datetime.timedelta(days=365))
        return date.fuzz().isoformat()

    def _create_event(self, today=False):
        # switch factory
        fac = Event_Factory
        if today:
            fac = Today_Event_Factory
        else:
            fac = Event_Factory
        e = fac.create()
        print("DEBUG: ", e.id)
        Event_Cache.update(e)
        print(Event_Cache.query.all())
        return e

    def test_empty_eventlist(self):
        r = self.client.get("/events/", follow_redirects=True)
        self.assert_200(r)

    def test_event_list(self):
        e = self._create_event(today=True)
        r = self.client.get("/events/", follow_redirects=True)
        self.assert_200(r)
        self.assertEqual(len(r.json['data']['events']), 1)
        self.assertEqual(r.json['data']['events'][0]['title'], e.title)

    def test_event_list_multiple(self):
        e1 = self._create_event(today=True)
        e2 = self._create_event(today=True)
        r = self.client.get("/events/", follow_redirects=True)
        self.assert_200(r)
        self.assertEqual(len(r.json['data']['events']), 2)
        self.assertEqual(r.json['data']['events'][0]['title'], e1.title)
        self.assertEqual(r.json['data']['events'][1]['title'], e2.title)

    def test_event_list_attributes(self):
        event = self._create_event(today=True)
        r = self.client.get("/events/", follow_redirects=True)
        self.assert_200(r)
        self.assertEqual(len(r.json['data']['events']), 1)
        revent = r.json['data']['events'][0]
        self.assertEqual(revent['title'], event.title)
        self.assertEqual(parse(revent['dtstart'], ignoretz=True), event.dtstart)
        self.assertEqual(revent['desc'], event.desc)
        self.assertEqual(revent['subtitle'], event.subtitle)
        self.assertEqual(revent['tags'], event.tags)
        
    def test_post_event_create_new(self):
        data = dict(title="MyEvent", subtitle="Simple Event", id=1,
                    location=dict(id=23, name='somewhere'),
                    dtstart=str(self._create_date()))
        print( "DICT", data)
        print( "JSON", json.dumps(data))
        response = self.client.post('/events/', data=json.dumps(data),
                                    content_type='application/json')
        print(response.json)
        self.assert_200(response)
        revent = Event.query.all()[0]
        self.assertEqual(revent.title, "MyEvent")
        self.assertEqual(revent.subtitle, data['subtitle'])
        self.assertEqual(revent.dtstart, parse(data['dtstart']))
        self.assertEqual(revent.location_id, data['location']['id'])

    def test_post_event_modify(self):
        l1 = self._create_event()
        data = dict(id=l1.id, title="MyEvent", subtitle="Simple Event",
                    dtstart=l1.dtstart.isoformat(),
                    location=dict(id=23, name='somewhere')
        )
        response = self.client.post('/event/{0}'.format(l1.id), data=json.dumps(data),
                                     content_type='application/json')
        self.assert_200(response)
        self.assertEqual(Event.query.all()[0].title, "MyEvent")

    def test_post_event_modify_404(self):
        e1 = self._create_event()
        data = dict(id=2, title="MyEvent", subtitle="Simple Event", location=dict(id=23, name='somewhere'),)
        response = self.client.post('/event/2', data=json.dumps(data),
                                    content_type='application/json')
        self.assert_404(response)
        self.assertEqual(Event.query.all()[0].title, e1.title)

    def test_event_by_id(self):
        e = self._create_event()
        response = self.client.get('/event/{0}'.format(e.id))
        print(response.data)
        self.assert_200(response)
        print(response.json)
        json_response = response.json
        self.assertEqual(json_response['data']['title'], e.title)

    def test_event_create_range_recurring_days(self):
        dtstart = self._create_date()
        data = dict(title="MyEvent", subtitle="Simple Event",
                    location=dict(id=23, name='somewhere'),
                    dtstart=str(dtstart),
                    rrule = dict(freq='DAILY', count=3, dtstart=str(dtstart)))
        print( "DICT", data)
        print( "JSON", json.dumps(data))
        response = self.client.post('/events/', data=json.dumps(data),
                                    content_type='application/json')
        print(response.json)
        self.assert_200(response)
        self.assertEqual(Event.query.all()[0].title, "MyEvent")
        response = self.client.get('/events/')
        
        
