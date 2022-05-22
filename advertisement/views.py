from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from advertisement.models import Advertisement
from advertisement.serializers import AdvertisementSerializer
from advertisement.services import AdvertisementService
from user.permissions import IsAdmin


@extend_schema_view(
    list=extend_schema(
        summary='Список рекламных объявлений',
        tags=['advertisement'],
    ),
    retrieve=extend_schema(
        summary='Информация о рекламном объявлении',
        tags=['advertisement'],
    ),
    create=extend_schema(
        summary='Создание рекламного объявления',
        tags=['advertisement'],
    ),
    update=extend_schema(
        summary='Редактирование рекламного объявления',
        tags=['advertisement'],
    ),
    destroy=extend_schema(
        summary='Удаление рекламного объявления',
        tags=['advertisement'],
    ),
    watch_ad=extend_schema(
        request=None,
        responses={204: None},
        summary='Просмотр рекламы текущим пользователем',
        tags=['advertisement'],
    ),
)
class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve' | 'watch_ad':
                self.permission_classes = (IsAuthenticated,)
            case _:
                self.permission_classes = (IsAuthenticated, IsAdmin)
        return super(AdvertisementViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return self.queryset
        viewed_ads_id = self.request.user.viewed_ads.first().advertisements.values_list('id')
        return self.queryset.exclude(id__in=viewed_ads_id)

    @action(detail=True, methods=['post'], url_path='watch')
    def watch_ad(self, request, pk=None, *args, **kwargs):
        AdvertisementService.watch_ad(user=request.user, ad_id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
