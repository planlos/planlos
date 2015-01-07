from . import PlanlosApiTest
from app.models import User, Role
from app import db


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

        # create_some_events
        # factory_boy

    def _create_event(self):
        

        
    def test_eventlist(self):
        r = self.client.get("/events/", follow_redirects=True)
        self.assert_200(r)

    def test_post_event(self):
        data = dict(name="Jesse")
        response = self.client.post('/events/', data=data,
                                    content_type='application/json')
        self.assert_200(response)

    def test_event_by_date(self):
        response = self.client.get('/events/1')
        self.assert_200(response)
