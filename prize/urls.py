from django.urls import path, include
from rest_framework import routers

from prize.views import PrizeViewSet, PrizeRequestViewSet

router = routers.DefaultRouter()
router.register(r'request', PrizeRequestViewSet, basename='prize-request')
router.register(r'', PrizeViewSet, basename='prize')

urlpatterns = [
    path('prize/', include(router.urls))
]
