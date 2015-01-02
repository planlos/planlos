from . import PlanlosApiTest
from app.models import User, Role
from app import db
from app.services import users as userservice


class Test_User_Service(PlanlosApiTest):
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


    def test_login_user(self):
        user = userservice.find(username='test')
        assert user != None
        self.assertEqual(user.username, 'test')
