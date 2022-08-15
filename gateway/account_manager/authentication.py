from google.protobuf.json_format import ParseDict

# These protocol buffers are generated automatically
# for viewing protocol buffers go to the Protobuffs repository
# https://github.com/huma-challenge/Protobuffs/tree/main/account_manager
from protobufs.account_manager import account_pb2 as acc_typ


from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions


def get_authorization_header(request):
    """
    Return request's 'HTTP_USERTOKEN_AUTHORIZATION:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    return auth


class UserTokenAuthentication(TokenAuthentication):
    """DRF TokenAuthentication that uses HTTP_USERTOKEN_AUTHORIZATION header."""

    def authenticate(self, request):
        auth = get_authorization_header(request)

        if isinstance(auth, bytes):
            auth = auth.decode("utf-8")
        else:
            ...

        # if auth not provided does not set token attr to request
        if not auth:
            return

        token = auth
        user_token = ParseDict({"token": str(token)}, acc_typ.UserToken())
        request.token = user_token

        return
