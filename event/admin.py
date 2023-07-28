from django.contrib import admin

from event.models import ScheduleAvailable

@admin.register(ScheduleAvailable)
class ScheduleAvailableAdmin(admin.ModelAdmin):
    list_display = (
        "user",
    )

