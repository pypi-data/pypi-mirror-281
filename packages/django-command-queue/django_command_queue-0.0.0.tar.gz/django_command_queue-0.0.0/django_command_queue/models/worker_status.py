__all__ = ["WorkerStatus"]

from django.db import models


class WorkerStatus(models.Model):
    id = models.AutoField(primary_key=True)
    worker = models.OneToOneField(
        "Worker", related_name="+", on_delete=models.DO_NOTHING
    )
    started_at = models.FloatField()
    updated_at = models.FloatField(null=True)

    class Meta:
        db_table = "django_command_queue_worker_status"
