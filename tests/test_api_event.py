from . import PlanlosApiTest
from app.models import User, Role
from app.models.events import Event
from app.models.events import Event_Cache
from app.models.location import Location
from app import db

import factory
import factory.alchemy
import factory.fuzzy

import datetime
import json


class Event_Factory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = db.session

    # id = 1 ## _sequence als kwarg
    id = factory.Sequence(lambda n: n)
    title = factory.fuzzy.FuzzyText(length=20, prefix="Event_")
    subtitle = "kurz"
    desc = "Beschreibung"
    dtstart = factory.fuzzy.FuzzyDate(datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(days=365))


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
        db.session.remove()
        db.drop_all()

    def _create_event(self):
        e = Event_Factory.create()
        print("DEBUG: ", e.id)
        Event_Cache.update(e)
        print(Event_Cache.query.all())
        return e

    def test_eventlist(self):
        self._create_event()
        r = self.client.get("/events/", follow_redirects=True)
        self.assert_200(r)

    def test_event_list(self):
        e = self._create_event()
        r = self.client.get("/events/", follow_redirects=True)
        self.assert_200(r)
        self.assertEqual(len(r.json['events']), 1)
        self.assertEqual(r.json['events'][0]['title'], e.title)

    def test_event_list_multiple(self):
        e1 = self._create_event()
        e2 = self._create_event()
        r = self.client.get("/events/", follow_redirects=True)
        self.assert_200(r)
        self.assertEqual(len(r.json['events']), 2)
        self.assertEqual(r.json['events'][0]['title'], e1.title)
        self.assertEqual(r.json['events'][1]['title'], e2.title)


    def test_post_event_create_new(self):
        data = dict(title="MyEvent", subtitle="Simple Event", id=1)
        response = self.client.post('/events/', data=json.dumps(data),
                                   content_type='application/json')
        self.assert_200(response)
        self.assertEqual(Event.query.all()[0].title, "MyEvent")

    def test_post_event_modify(self):
        l1 = self._create_event()
        data = dict(id=1, title="MyEvent", subtitle="Simple Event")
        response = self.client.patch('/events/1', data=json.dumps(data),
                                     content_type='application/json')
        self.assertEqual(response, 201)
        self.assertEqual(Event.query.all()[0].title, "MyEvent")

    def test_post_event_modify_404(self):
        e1 = self._create_event()
        data = dict(id=2, title="MyEvent", subtitle="Simple Event")
        response = self.client.patch('/events/2', data=json.dumps(data),
                                     content_type='application/json')
        self.assert_404(response)
        self.assertEqual(Event.query.all()[0].title, e1.title)

    def test_event_by_id(self):
        e = self._create_event()
        response = self.client.get('/events/{0}'.format(e.id))
        self.assert_200(response)
        print(response.json)
        json_response = response.json
        self.assertEqual(json_response['event']['title'], e.title)
