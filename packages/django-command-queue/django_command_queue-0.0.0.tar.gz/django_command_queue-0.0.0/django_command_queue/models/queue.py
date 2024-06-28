__all__ = ["Queue"]

from django.db import models


class Queue(models.Model):
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey(
        "Worker", related_name="+", on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=255,unique=True)

    class Meta:
        db_table = "django_command_queue"
        unique_together = [('worker', 'name',)]
