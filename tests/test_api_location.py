from . import PlanlosApiTest
from app.models import User, Role
from app.models.location import Location
from app.models.location import Photo
from app import db
import json

import factory
import factory.alchemy
import factory.fuzzy


class Location_Factory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Location
        sqlalchemy_session = db.session

    #id = 1 ## _sequence als kwarg
    name = factory.fuzzy.FuzzyText(length=20,prefix="Location_")
    shortdesc = "This ist noob"


class Test_Location_Api(PlanlosApiTest):
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

        # create_some_events
        # factory_boy

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_location(self):
        l = Location_Factory.create()
        return l

    def test_location_list(self):
        l = self._create_location()
        r = self.client.get("/locations/", follow_redirects=True)
        self.assert_200(r)
        self.assertEqual(len(r.json['locations']), 1)
        self.assertEqual(r.json['locations'][0]['name'], l.name)

    def test_location_list_multiple(self):
        l1 = self._create_location()
        l2 = self._create_location()
        r = self.client.get("/locations/", follow_redirects=True)
        self.assert_200(r)
        self.assertEqual(len(r.json['locations']), 2)
        self.assertEqual(r.json['locations'][0]['name'], l1.name)
        self.assertEqual(r.json['locations'][1]['name'], l2.name)


    def test_post_location_create_new(self):
        data = dict(name="MyLocation", shortdesc="Simple Location", id=1)
        response = self.client.post('/locations/', data=json.dumps(data),
                                   content_type='application/json')
        self.assert_200(response)
        self.assertEqual(Location.query.all()[0].name, "MyLocation")

    def test_post_location_modify(self):
        l1 = self._create_location()
        data = dict(id=1, name="MyLocation", shortdesc="Simple Location")
        response = self.client.patch('/locations/1', data=json.dumps(data),
                                     content_type='application/json')
        self.assertEqual(response, 201)
        self.assertEqual(Location.query.all()[0].name, "MyLocation")

    def test_post_location_modify_404(self):
        l1 = self._create_location()
        data = dict(id=2, name="MyLocation", shortdesc="Simple Location")
        response = self.client.patch('/locations/2', data=json.dumps(data),
                                     content_type='application/json')
        self.assert_404(response)
        self.assertEqual(Location.query.all()[0].name, l1.name)

    def test_location_by_id(self):
        l = self._create_location()
        response = self.client.get('/locations/1')
        self.assert_200(response)
        print(response.json)
        json_response = response.json
        self.assertEqual(json_response['location']['name'], l.name)
