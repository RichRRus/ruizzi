from django.urls import path, include
from rest_framework import routers

from .views import AdvertisementViewSet

router = routers.DefaultRouter()
router.register(r'', AdvertisementViewSet, basename='user')

urlpatterns = [
    path('advertisement/', include(router.urls))
]
