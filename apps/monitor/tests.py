from django.test import TestCase
from apps.checks.models import CheckConfig
from apps.monitor.views import run_checks


class TestRunOne(TestCase):
    def test_create(self):
        flow = {'and': [{'name': 'some', 'type': 'test'}]}
        u = CheckConfig(id='check_id', name='check', config={}, flow=flow, location='location')
        u.save()
        self.assert_(u.pk is not None)
        try:
            run_checks(check_id='check_id')
            self.assert_(True)
        except:
            self.assert_(False)

