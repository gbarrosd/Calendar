from rest_framework.routers import SimpleRouter, DefaultRouter
from user.api.views import (
    UserRegistrationViewSet,
    UserViewSet,
)

router = DefaultRouter(trailing_slash=False)

router.register(r"users", UserViewSet, basename='user')
router.register(r"register", UserRegistrationViewSet, basename='user_registration')