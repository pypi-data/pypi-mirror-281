from django.contrib import admin

from ..models import Worker as Model


class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "restart_interval",
        "sleep_interval",
    ]
    search_fields = [
        "name",
    ]

admin.site.register(Model, ModelAdmin)
