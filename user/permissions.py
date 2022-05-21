from rest_framework import permissions

from user.models import User


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user:
            return request.user.is_superuser or request.user.is_admin
        return False


class IsCurrentUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.parser_context.get('kwargs') and (pk := request.parser_context.get('kwargs').get('pk')):
            obj = User.objects.filter(pk=pk).first()
            return obj == request.user
        return False

    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj == request.user
        return False
