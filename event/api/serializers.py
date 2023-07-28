from rest_framework import serializers
from user.api.serializers import UserListSerializer
from django.contrib.auth import get_user_model
from event.models import ScheduleAvailable

User = get_user_model()


class CreateScheduleAvailableSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ScheduleAvailable
        fields = "__all__"

class ScheduleAvailableSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = ScheduleAvailable
        fields = "__all__"
        depth = 1 

class CreateEventSerializer(serializers.Serializer):
    summary = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    description = serializers.CharField()
    start = serializers.DateTimeField()
    duration = serializers.IntegerField(required=False)


class MakeAppointmentSerializer(serializers.Serializer):
    summary = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    description = serializers.CharField()
