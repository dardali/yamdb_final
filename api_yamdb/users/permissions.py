from rest_framework.permissions import BasePermission

from users.models import User


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff
            or request.user.is_superuser
            or request.user.role == User.ROLE_ADMIN
        )
