from . import PlanlosApiTest
from app.models.location import Location
from app.models import User, Role
from app import db
import json

from app.api.schemas import Location_Schema

from flask import jsonify

import factory
import factory.alchemy
import factory.fuzzy


class Location_Factory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Location
        sqlalchemy_session = db.session

    # id = 1 ## _sequence als kwarg
    name = factory.fuzzy.FuzzyText(length=20, prefix="Location_")
    shortdesc = "This ist noob"


class Test_Schemas(PlanlosApiTest):
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

    def test_schema_validation(self):
        schema = Location_Schema()
        data = dict(name="MyLocation", shortdesc="Simple Location", id=1)
        error = schema.validate(data)
        self.assertEqual(error, {})

    def test_schema_validation_fail(self):
        schema = Location_Schema()
        data = dict(shortdesc="Simple Location", id=1, is_pub=True)
        error = schema.validate(data)
        self.assertEqual(error, {'name': ['Missing data for required field.']})
