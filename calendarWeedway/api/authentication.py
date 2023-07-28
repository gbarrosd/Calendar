from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed

class GoogleAuthentication(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'credentials' in request.session:

            return True

        raise AuthenticationFailed('Usuário não autenticado com o Google.')


