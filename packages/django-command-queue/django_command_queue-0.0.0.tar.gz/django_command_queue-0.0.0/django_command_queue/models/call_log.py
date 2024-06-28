__all__ = ["CallLog"]

from django.db import models


class CallLog(models.Model):
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey(
        "Worker", related_name="+", on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=255)
    created_at = models.IntegerField()

    class Meta:
        db_table = "django_command_queue_call_log"
