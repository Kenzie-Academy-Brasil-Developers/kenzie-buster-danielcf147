from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Movie


class IsAdmOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        print("IsAdminOrReadOnly executado")
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_staff
        )
