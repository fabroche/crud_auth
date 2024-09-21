from rest_framework.permissions import BasePermission


class IsPersona(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="doctors").exists()
