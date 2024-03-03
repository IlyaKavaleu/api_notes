from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor_Or_ReadOnly(BasePermission):
    def has_permission(self, request, view):
        """First check"""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """After first check, we checking obj"""
        if request.method in SAFE_METHODS:
            return True
        else:
            if obj.author == request.user:
                return True
            else:
                return False
