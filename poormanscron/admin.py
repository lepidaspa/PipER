from django.contrib import admin
from django.db import models
ScheduledTask = models.get_model("poormanscron", "ScheduledTask")

class ScheduledTaskOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ("__unicode__", "frequency_admin_display", "is_active", "is_heavy", "ready_admin_display")
    list_filter = ("is_active", "is_heavy")
admin.site.register(ScheduledTask, ScheduledTaskOptions)
