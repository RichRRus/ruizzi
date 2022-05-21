from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('user/', include(router.urls))
]
