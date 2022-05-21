from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from prize.models import Prize
from prize.serializers import PrizeSerializer
from user.permissions import IsAdmin


@extend_schema_view(
    list=extend_schema(
        summary='Список подарков',
        tags=['prize'],
    ),
    retrieve=extend_schema(
        summary='Информация о подарке',
        tags=['prize'],
    ),
    create=extend_schema(
        summary='Создание приза',
        tags=['prize'],
    ),
    put=extend_schema(
        summary='Редактирование приза',
        tags=['prize'],
    ),
    delete=extend_schema(
        summary='Удаление приза',
        tags=['prize'],
    ),
)
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
