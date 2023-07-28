from rest_framework.routers import SimpleRouter, DefaultRouter
from event.api.views import (
    CreateEventViewSet,
    GoogleCalendarViewSet, 
    SchedulesViewSet,
)

router = DefaultRouter(trailing_slash=False)

router.register(r"event", CreateEventViewSet, basename='event')
router.register(r"google-calendar", GoogleCalendarViewSet, basename='login_with_google')
router.register(r"schedules-available", SchedulesViewSet, basename='schedules-available')