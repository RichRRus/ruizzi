from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user import permissions, serializers
from user.models import User
from user.services import UserService


@extend_schema_view(
    list=extend_schema(
        summary='Список пользователей',
        tags=['user'],
    ),
    retrieve=extend_schema(
        summary='Информация о пользователе',
        tags=['user'],
    ),
    create=extend_schema(
        responses=serializers.UserSerializer,
        summary='Регистрация пользователя',
        tags=['user'],
    ),
)
class UserViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_serializer_class(self):
        match self.action:
            case 'create':
                return serializers.UserCreateSerializer
            case _:
                return self.serializer_class

    def get_permissions(self):
        match self.action:
            case 'create':
                self.permission_classes = []
            case 'list':
                self.permission_classes = [IsAuthenticated & permissions.IsAdmin]
            case 'retrieve':
                self.permission_classes = [(permissions.IsAdmin | permissions.IsCurrentUser)]
            case _:
                self.permission_classes = [IsAuthenticated]
        return super(UserViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        serializer = self.serializer_class(instance=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        data = serializer.data
        return UserService.create_user(email=data.pop('email'), password=data.pop('password'), **data)
