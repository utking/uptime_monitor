from django.test import TestCase
from .models import ScheduleItem
from apps.checks.models import CheckConfig


class TestSchedule(TestCase):
    def test_create(self):
        check = CheckConfig(name='check', config={}, flow={}, location='location')
        check.save()
        u = ScheduleItem(name='check', check_id=check, schedule='* * * * *')
        u.save()
        self.assert_(u.pk > 0)
