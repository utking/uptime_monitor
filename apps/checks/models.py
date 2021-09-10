from django.db import models


class CheckConfig(models.Model):
    id = models.CharField(primary_key=True, max_length=64, unique=True)
    name = models.CharField(max_length=64, unique=True)
    location = models.CharField(max_length=128, default='none')
    config = models.JSONField(max_length=1024)
    flow = models.JSONField(max_length=2048, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class CheckHistory(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    check_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=128)
    success = models.BooleanField()
    resp_code = models.IntegerField(null=True)
    timings = models.JSONField(default=list)
    result = models.CharField(max_length=4096)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['check_id']),
        ]
