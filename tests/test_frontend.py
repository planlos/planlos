from . import PlanlosFrontendTest
from app.models import User, Role
from app import db


class Test_Frontend(PlanlosFrontendTest):
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

    def test_appcreation(self):
        assert(self.app is not None)

    def test_index(self):
        r = self.client.get("/", follow_redirects=True)
        self.assert_200(r)
        # self.assert_context("current_user", "AnonymousUser")
        self.assert_template_used("events/index.html")
