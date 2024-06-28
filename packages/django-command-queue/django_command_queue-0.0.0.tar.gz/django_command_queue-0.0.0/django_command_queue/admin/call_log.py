from django.contrib import admin

from ..models import CallLog as Model


class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "worker",
        "name",
        "datetime",
        "timesince",
    ]
    list_filter = [
        "worker",
    ]
    search_fields = [
        "name",
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
