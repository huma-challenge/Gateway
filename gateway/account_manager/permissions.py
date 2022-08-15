from rest_framework import permissions
from django.http.request import HttpRequest


class RequestHaveToken(permissions.BasePermission):
    message = "Reqeust Have Token"

    def has_object_permission(self, request: HttpRequest, view, obj):
        return hasattr(request, "token")
