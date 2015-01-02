from . import PlanlosApiTest


class Test_App(PlanlosApiTest):

    def test_appcreation(self):
        assert(self.app is not None)
