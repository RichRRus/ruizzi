from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from prize.models import Prize
from prize.serializers import PrizeSerializer
from user.permissions import IsAdmin


class PrizeViewSet(viewsets.ModelViewSet):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve':
                self.permission_classes = (IsAuthenticated,)
            case _:
                self.permission_classes = (IsAuthenticated, IsAdmin)
        return super(PrizeViewSet, self).get_permissions()
