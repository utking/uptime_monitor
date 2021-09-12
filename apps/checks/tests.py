from django.test import TestCase
from .models import CheckConfig, CheckHistory


class TestConfig(TestCase):
    def test_create(self):
        u = CheckConfig(name='check', config={}, flow={}, location='location')
        u.save()
        self.assert_(u.pk is not None)


class TestHistory(TestCase):
    def test_create(self):
        u = CheckHistory(check_id='check_id', name='name', success=True, location='location')
        u.save()
        self.assert_(u.pk > 0)
