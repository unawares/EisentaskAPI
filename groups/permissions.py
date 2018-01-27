from rest_framework import permissions

class GroupAdminAccessPermission(permissions.BasePermission):
    message = 'Admin actions are not allowed'

    def has_permission(self, request, view):
        return True
