from datetime import datetime

from flask.ext.security import SQLAlchemyUserDatastore
from flask.ext.testing import TestCase
from nose.tools import raises
from sqlalchemy.exc import IntegrityError

from app import assets, db
from app.api import create_app as app_factory
from app.config import Testing
from app.frontend import create_app as frontend_app_factory
from app.models import User, Role


# from app.factory import create_app as app_factory


class PlanlosApiTest(TestCase):
    def create_app(self):
        assets._named_bundles = {}
        return app_factory(settings_override=Testing())

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class PlanlosFrontendTest(TestCase):
    def create_app(self):
        assets._named_bundles = {}
        return frontend_app_factory(settings_override=Testing())

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestUserModel(PlanlosApiTest):
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

    def test_query_user(self):
        expected = [self.myuser]
        result = User.query.all()
        self.assertEqual(result, expected)

    def test_query_userrole(self):
        result = User.query.one()
        self.assertEqual(result.roles, [self.adminrole])

    def test_query_role(self):
        expected = [self.adminrole, self.editorrole]
        result = Role.query.all()
        self.assertEqual(result, expected)

    def test_modified_flag(self):
        d = datetime.now()
        self.myuser.username = 'peter'
        self.myuser.save()
        self.assertGreater(self.myuser.last_modified, d)

    @raises(IntegrityError)
    def test_create_unique_username(self):
        try:
            db.session.add(User(username='test', email='test@localhost', password='test'))
            db.session.commit()
        except:
            db.session.rollback()
            raise

    @raises(IntegrityError)
    def test_create_unique_email(self):
        try:
            db.session.add(User(username='test2', email='test@localhost', password='test'))
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def test_user_has_role(self):
        assert(self.myuser.has_role(self.adminrole))

    def test_userdatastore(self):
        ds = SQLAlchemyUserDatastore(db, User, Role)
        ds.create_user(username='test2', email='test2@localhost', password='test2')
        result = User.query.filter_by(username='test2')
        self.assertEqual(result[0].username, 'test2')

        ds.add_role_to_user(self.myuser, self.editorrole)
        result = User.query.filter_by(username='test')
        assert(self.editorrole in result[0].roles)
        assert(self.adminrole in result[0].roles)
        ds.remove_role_from_user(self.myuser, self.editorrole)
        ds.activate_user(self.myuser)
