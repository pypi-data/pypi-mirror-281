from django.contrib import admin

from ..models import Queue as Model


class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
    search_fields = [
        "name",
    ]


admin.site.register(Model, ModelAdmin)
