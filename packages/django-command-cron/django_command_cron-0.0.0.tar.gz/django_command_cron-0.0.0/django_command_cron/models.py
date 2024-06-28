__all__ = ["CommandCron"]

from django.db import models


class CommandCron(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    interval = models.FloatField()
    called_at = models.FloatField(null=True)

    class Meta:
        db_table = 'django_command_cron'
