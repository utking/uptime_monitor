from django.test import TestCase
from apps.checks.models import CheckConfig
from apps.monitor.views import run_checks


class TestRunOne(TestCase):
    def test_create(self):
        flow = {'type': 'and', 'elements': [{'name': 'some', 'type': 'test'}]}
        u = CheckConfig(id='check_id', name='check', config={}, flow=flow, location='location')
        u.save()
        self.assert_(u.pk is not None)
        run_checks(check_id='check_id')
        self.assert_(True)

    def test_run_http_check(self):
        flow = {'type': 'and', 'elements': [
            {'name': 'some', 'type': 'http_ping', 'url': 'http://fake'}
        ]}
        u = CheckConfig(id='check_http', name='check', config={}, flow=flow, location='location')
        u.save()
        self.assert_(u.pk is not None)
        ret = run_checks(check_id='check_http')
        self.assert_(ret)

    def test_run_http_check_fail(self):
        flow = {'type': 'and', 'elements': [
            {'name': 'some', 'type': 'http_ping'}
        ]}
        u = CheckConfig(id='check_http', name='check', config={}, flow=flow, location='location')
        u.save()
        self.assert_(u.pk is not None)
        ret = run_checks(check_id='check_http')
        self.assert_(not ret)
