from . import PlanlosApiTest
from app.models import User, Role
from flask.ext.security.core import current_user
from app import db
from app import security

import datetime

class Test_Security(PlanlosApiTest):
    def setUp(self):
        super().setUp()
        self.myuser = User(username='test', email='test@localhost', password='test')
        # self.myuser.active = True
        self.adminrole = Role(name='admin', description='Admin User')
        self.editorrole = Role(name='editor', description='Editor')
        self.myuser.roles = [self.adminrole]
        self.myuser.confirmed_at = datetime.datetime.now()
        db.session.add(self.myuser)
        db.session.add(self.adminrole)
        db.session.add(self.editorrole)
        db.session.commit()

    def test_appcreation(self):
        assert(self.app is not None)

    def test_security_plugin(self):
        assert(security is not None)

    def test_security_login(self):
        r = self.client.get("/login")
        self.assert_200(r)

    def test_security_login_user_not_activated(self):
        with self.client:
            r = self.client.post("/login", data=dict(email='test@localhost', password='test', remember=False),
                                 follow_redirects=False)
            self.assert200(r)
            self.assertTrue(current_user.is_anonymous())

    def test_security_login_user_activated(self):
        with self.client:
            self.myuser.active = True
            db.session.add(self.myuser)
            db.session.commit()
            r = self.client.post("/login", data=dict(email='test@localhost', password='test', remember=False),
                                 follow_redirects=False)
            self.assertRedirects(r, '/')
            assert(current_user.email == 'test@localhost')
            assert(current_user.get_auth_token() is not None)

    def test_security_logout(self):
        with self.client:
            r = self.client.get("/logout")
            self.assertRedirects(r, "/")
            self.assertTrue(current_user.is_anonymous())
