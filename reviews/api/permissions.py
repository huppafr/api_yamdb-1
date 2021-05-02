from django.conf import settings
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.role in (settings.ADMIN, settings.MODERATOR)
                or request.user.is_superuser
                or obj.author == request.user)
