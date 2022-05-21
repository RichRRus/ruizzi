from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from prize.models import Prize, PrizeRequest
from prize.serializers import PrizeSerializer, PrizeRequestSerializer, PrizeRequestCreateSerializer
from prize.services import PrizeRequestService
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
    update=extend_schema(
        summary='Редактирование приза',
        tags=['prize'],
    ),
    destroy=extend_schema(
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


@extend_schema_view(
    list=extend_schema(
        summary='Список заявок на получение подарков',
        tags=['prize-request'],
    ),
    retrieve=extend_schema(
        summary='Информация о заявке на получение подарка',
        tags=['prize-request'],
    ),
    create=extend_schema(
        responses=PrizeRequestSerializer,
        summary='Создание заявки на получение подарка',
        tags=['prize-request'],
    ),
    reject=extend_schema(
        request=None,
        responses={204: None},
        summary='Отклонение заявки',
        tags=['prize-request'],
    ),
    accept=extend_schema(
        request=None,
        responses={204: None},
        summary='Принять заявку в работу',
        tags=['prize-request'],
    ),
    done=extend_schema(
        request=None,
        responses={204: None},
        summary='Завершить заявку',
        tags=['prize-request'],
    ),
    get_user_requests=extend_schema(
        request=None,
        responses=PrizeRequestSerializer(many=True),
        summary='Список заявок пользователя',
        tags=['prize-request'],
    )
)
class PrizeRequestViewSet(viewsets.ModelViewSet):
    queryset = PrizeRequest.objects.all()
    serializer_class = PrizeRequestSerializer
    http_method_names = ['get', 'post']

    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve' | 'create' | 'get_user_requests':
                self.permission_classes = (IsAuthenticated,)
            case _:
                self.permission_classes = (IsAuthenticated, IsAdmin)
        return super(PrizeRequestViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        match self.action:
            case 'create':
                return PrizeRequestCreateSerializer
            case _:
                return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prize_request = self.perform_create(serializer)
        serializer = PrizeRequestSerializer(instance=prize_request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None, *args, **kwargs):
        PrizeRequestService.reject_request(request_id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None, *args, **kwargs):
        PrizeRequestService.accept_request(request_id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def done(self, request, pk=None, *args, **kwargs):
        PrizeRequestService.done_request(request_id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='me')
    def get_user_requests(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        prize_request = PrizeRequestService.create_request(
            user=self.request.user,
            prize_id=self.request.data.get('prize')
        )
        return prize_request
