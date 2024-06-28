from datetime import datetime
from django.contrib import admin
from django.utils.timesince import timesince

from ..models import WorkerException as Model


class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "worker",
        "exc_class",
        "exc_message",
        "datetime",
        "timesince",
    ]
    search_fields = [
        "name",
        "exc_class",
        "exc_message",
        "exc_traceback",
    ]

    def datetime(self, obj):
        return datetime.fromtimestamp(obj.created_at)

    def timesince(self, obj):
        return timesince(datetime.fromtimestamp(obj.created_at)).split(',')[0]+' ago'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



admin.site.register(Model, ModelAdmin)
