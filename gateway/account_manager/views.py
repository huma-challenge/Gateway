from drf_spectacular.utils import extend_schema

from gateway.account_manager.grcp_app import get_grcp_manager
from gateway.account_manager.serializer import (
    UserLogin,
    UserLoginResponse,
    UserProtoSerializer,
)

from google.protobuf.json_format import MessageToDict, ParseDict

# These protocol buffers are generated automatically
# for viewing protocol buffers go to the Protobuffs repository
# https://github.com/huma-challenge/Protobuffs/tree/main/account_manager
from protobufs.account_manager import account_pb2 as acc_typ
from protobufs.account_manager import account_pb2_grpc as acc_grpc

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

# Generate A gRPC manager based on the app
grcp_manager = get_grcp_manager()

# generate client and register on the app channel
def generate_user_manager_stub() -> acc_grpc.UserManagerStub:
    return grcp_manager.create_new_client(acc_grpc.UserManagerStub)


from gateway.account_manager.authentication import UserTokenAuthentication
from gateway.account_manager.permissions import RequestHaveToken


class AccountManager(ViewSet):
    authentication_classes = (UserTokenAuthentication,)
    serializer_class = UserProtoSerializer

    def get_permissions(self):
        permission_classes = ()

        # A list of method that dons't need token in ther reqeust header
        METHODS_WITHOUT_TOKEN = ["create", "login"]

        if self.action not in METHODS_WITHOUT_TOKEN:
            permission_classes = (RequestHaveToken,)

        return [permission() for permission in permission_classes]

    @extend_schema(summary="Fetch All Users")
    def list(self, request):
        client = generate_user_manager_stub()

        # Generate RPC Request
        request_list = acc_typ.UserListRequest()
        request_list.token.CopyFrom(request.token)

        # fetch all users and convert from message to a list of dict
        try:
            user_list = [
                MessageToDict(user, True) for user in client.List(request_list)
            ]
        except:
            return Response(
                "Error while fechting users ", status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(user_list, status.HTTP_200_OK)

    @extend_schema(summary="Rmove User By User ID")
    def destroy(self, request, pk):
        client = generate_user_manager_stub()

        # Generate RPC Request
        request_destroy = acc_typ.UserDestroyRequest()
        request_destroy.token.CopyFrom(request.token)
        request_destroy.user_id = int(pk)

        try:
            client.Destroy(request_destroy)
        except:
            return Response(
                "Error while removing user", status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response("User Removed", status.HTTP_200_OK)

    @extend_schema(summary="Retrieve User By User ID")
    def retrieve(self, request, pk):
        client = generate_user_manager_stub()

        # Generate RPC Request
        request_user_retrieve = acc_typ.UserRetrieveRequest()
        request_user_retrieve.user_id = int(pk)
        request_user_retrieve.token.CopyFrom(request.token)

        try:
            result = MessageToDict(client.Retrieve(request_user_retrieve))
        except:
            return Response("User does not exist", status.HTTP_404_NOT_FOUND)

        return Response(result, status.HTTP_200_OK)

    @extend_schema(summary="Update User By User ID")
    def update(self, request, pk):
        client = generate_user_manager_stub()

        # Generate User Message from input data
        user_data = request.data
        user_message = ParseDict(user_data, acc_typ.User())

        # Generate RPC Request
        request_user_update = acc_typ.UserUpdateRequest()
        request_user_update.user.CopyFrom(user_message)
        request_user_update.token.CopyFrom(request.token)

        try:
            result = MessageToDict(client.Update(request_user_update))
        except:
            return Response(
                "Error while updating user", status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(result, status.HTTP_200_OK)

    @extend_schema(summary="Create New User")
    def create(self, request):
        client = generate_user_manager_stub()

        # Generate User Message from input data
        user_data = request.data
        user_message = ParseDict(user_data, acc_typ.User())

        try:
            result = MessageToDict(client.Create(user_message))
        except:
            return Response(
                "Error while creating user", status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(result, status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def login(self, request):
        client = generate_user_manager_stub()

        # Generate User Message from input data
        user_data = request.data
        user_login_message_request = ParseDict(user_data, acc_typ.UserLoginRequest())

        try:
            result = MessageToDict(client.Login(user_login_message_request))
        except:
            return Response(
                "Error while login user", status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(result, status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def logout(self, request):
        client = generate_user_manager_stub()

        # Generate RPC Request
        request_logout = acc_typ.UserLogoutRequest()
        request_logout.token.CopyFrom(request.token)

        try:
            result = MessageToDict(client.Logout(request_logout))
        except:
            return Response(
                "Error while logout user", status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response("Logout is successfully ", status.HTTP_200_OK)
