from rest_framework import permissions
from django.http.request import HttpRequest


class RequestHaveToken(permissions.BasePermission):
    message = "The Request Header Does Not Have Token"

    def has_permission(self, request: HttpRequest, view):
        return False
        return hasattr(request, "token")
