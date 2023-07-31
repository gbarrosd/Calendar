from rest_framework import permissions, viewsets, filters, status, response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from calendarWeedway.mixins.mixins import GetSerializerClassMixin
from calendarWeedway.api.authentication import GoogleAuthentication
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from user.logic import create_event

from event.models import ScheduleAvailable


from event.api.serializers import (
    CreateEventSerializer,
    ScheduleAvailableSerializer,
    CreateScheduleAvailableSerializer,
    MakeAppointmentSerializer,
)

class GoogleCalendarViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def connect_google_calendar(self, request):

        return HttpResponseRedirect(reverse('calendar_init'))
    

class SchedulesViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = ScheduleAvailable.objects.filter(occupy=False)
    serializer_class = ScheduleAvailableSerializer
    serializer_action_classes = {
        "schedule": MakeAppointmentSerializer,
        "create": CreateScheduleAvailableSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = {
        "date": ['gte', 'lte'],
        "start_time": ["gte"], "end_time": ["lte"],  
    }
    search_fields = ["comments"]

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def schedule(self, request, pk):
        schedule = create_event(request, pk)

        return response.Response({"event": schedule})


class CreateEventViewSet(viewsets.ViewSet):
    permission_classes = [GoogleAuthentication]
    serializer_class = CreateEventSerializer

    @swagger_auto_schema(
        request_body=CreateEventSerializer,
        responses={status.HTTP_201_CREATED: 'Evento criado com sucesso!'}
    )

    def create(self, request):
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = create_event(request)

        if "Erro" in result:
            error_message = result["Erro"]
            return response.Response({"message": "Ocorreu um erro ao criar o evento", "Erro": error_message})
        
        return response.Response({"message": "Evento criado com sucesso!", "event": result})

    
