from rest_framework import permissions, viewsets
from django.contrib.auth import get_user_model

User = get_user_model()

from user.api.serializers import (
    UserListSerializer, 
    UserRegistrationSerializer,
)


class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['post']

    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    serializer_action_classes = {
        'list': UserListSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]



