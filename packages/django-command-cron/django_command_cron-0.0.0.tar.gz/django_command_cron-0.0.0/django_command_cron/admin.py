from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from .models import CommandCron as Model


class ModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "interval",
        "called_at",
        "called_at_datetime",
        "called_at_timesince",
    ]
    search_fields = [
        "name",
    ]

    def called_at_datetime(self, obj):
        if obj.called_at:
            return datetime.fromtimestamp(obj.called_at)
    called_at_datetime.short_description = "called datetime"

    def called_at_timesince(self, obj):
        if obj.called_at:
            return "%s ago" % timesince(datetime.fromtimestamp(obj.called_at))
    called_at_timesince.short_description = "called timesince"


admin.site.register(Model, ModelAdmin)
