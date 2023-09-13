from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwner(permissions.BasePermission):
    message = "Вы не являетесь владельцем данной привычки."

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        raise PermissionDenied(self.message)
