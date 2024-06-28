__all__ = ["Worker"]

from django.db import models


class Worker(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    restart_interval = models.FloatField(null=True)
    sleep_interval = models.FloatField(null=True)

    class Meta:
        db_table = "django_command_queue_worker"

    def __str__(self):
        return self.name
