from rest_framework import permissions
from django.http.request import HttpRequest

# These protocol buffers are generated automatically
# for viewing protocol buffers go to the Protobuffs repository
# https://github.com/huma-challenge/Protobuffs/tree/main/account_manager
from protobufs.account_manager import account_pb2 as acc_typ


class RequestHaveToken(permissions.BasePermission):
    message = "The Request Header Does Not Have Token"

    def has_permission(self, request: HttpRequest, view):
        if hasattr(request, "token"):
            return isinstance(request.token, acc_typ.UserToken)
        return False
