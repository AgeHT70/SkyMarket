# TODO здесь производится настройка пермишенов для нашего проекта
from rest_framework import permissions

from users.models import UserRoles


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.ADMIN
