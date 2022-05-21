from django.urls import path, include
from rest_framework import routers

from prize.views import PrizeViewSet

router = routers.DefaultRouter()
router.register(r'', PrizeViewSet, basename='user')

urlpatterns = [
    path('prize/', include(router.urls))
]
