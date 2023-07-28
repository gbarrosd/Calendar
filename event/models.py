from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ScheduleAvailable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="available_schedules")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    comments = models.CharField(blank=True, null=True)
    occupy = models.BooleanField(default=False)

