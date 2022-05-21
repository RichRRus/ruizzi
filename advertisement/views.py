from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from advertisement.models import Advertisement
from advertisement.serializers import AdvertisementSerializer
from user.permissions import IsAdmin


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve':
                self.permission_classes = (IsAuthenticated,)
            case _:
                self.permission_classes = (IsAuthenticated, IsAdmin)
        return super(AdvertisementViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return self.queryset
        viewed_ads_id = self.request.user.viewed_ads.first().advertisements.values_list('id')
        return self.queryset.exclude(id__in=viewed_ads_id)
