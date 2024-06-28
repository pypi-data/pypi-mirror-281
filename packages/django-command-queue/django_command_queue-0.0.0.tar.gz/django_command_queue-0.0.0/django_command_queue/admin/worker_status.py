from datetime import datetime
from django.contrib import admin
from django.utils.timesince import timesince

from ..models import WorkerStatus as Model


class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "worker",
        "started_at_datetime",
        "started_at_timesince",
        "updated_at_datetime",
        "updated_at_timesince",
    ]

    def started_at_datetime(self, obj):
        return datetime.fromtimestamp(obj.started_at)
    started_at_datetime.short_description = 'started datetime'

    def started_at_timesince(self, obj):
        return timesince(datetime.fromtimestamp(obj.started_at)).split(',')[0]+' ago'
    started_at_timesince.short_description = 'started timesince'

    def updated_at_datetime(self, obj):
        return datetime.fromtimestamp(obj.updated_at)
    updated_at_datetime.short_description = 'updated datetime'

    def updated_at_timesince(self, obj):
        return timesince(datetime.fromtimestamp(obj.updated_at)).split(',')[0]+' ago'
    updated_at_timesince.short_description = 'updated timesince'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Model, ModelAdmin)
