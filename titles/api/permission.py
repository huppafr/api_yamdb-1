from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and obj.author == request.user)


class IsModerator(BasePermission):
    message = 'Нужны права Модератора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moderator


class IsAdmin(BasePermission):
    message = 'Нужны права Администратора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    message = 'Нужны права Администратора'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsSuperuser(BasePermission):
    message = 'Нужны права Администратора Django'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.is_superuser)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение на уровне объекта, позволяющее только владельцам объекта
    редактировать его"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsSUandAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            try:
                if (request.user.role in ('admin') or request.user.is_superuser):
                    return True
            except AttributeError:
                return False
        else:
            return True