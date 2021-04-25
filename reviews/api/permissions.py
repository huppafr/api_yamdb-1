from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        if request.user.role in ('admin', 'moderator'):
            return True

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
