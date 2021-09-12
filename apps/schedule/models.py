from django.db import models
from apps.checks.models import CheckConfig
from croniter import croniter


class ScheduleItem(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=64, unique=True)
    check_id = models.OneToOneField(CheckConfig, on_delete=models.CASCADE)
    schedule = models.CharField(max_length=64, default='* * * * *')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not croniter.is_valid(self.schedule):
            raise Exception('"{}" is not a valid Cron schedule'.format(self.schedule))
        else:
            super(ScheduleItem, self).save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['check_id']),
        ]
