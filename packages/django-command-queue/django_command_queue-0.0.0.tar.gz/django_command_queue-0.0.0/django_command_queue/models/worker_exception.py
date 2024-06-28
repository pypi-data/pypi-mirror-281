__all__ = ["WorkerException"]

from django.db import models


class WorkerException(models.Model):
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey(
        "Worker", related_name="+", on_delete=models.DO_NOTHING
    )
    exc_class = models.CharField(max_length=255, verbose_name="Class")
    exc_message = models.TextField(verbose_name="Message")
    exc_traceback = models.TextField(verbose_name="Traceback")
    created_at = models.IntegerField()

    class Meta:
        db_table = "django_command_queue_worker_exception"
