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

from gateway.account_manager.grcp_app import get_grcp_manager

# Generate A gRPC manager based on the app
grcp_manager = get_grcp_manager()

# generate client and register on the app channel
def generate_user_manager_stub() -> acc_grpc.UserManagerStub:
    return grcp_manager.create_new_client(acc_grpc.UserManagerStub)


# Create Token for testing in development mode
request_login = acc_typ.UserLoginRequest()
request_login.username = "Ali"
request_login.password = "nova-man"
token = generate_user_manager_stub().Login(request_login)


class AccountManager(ViewSet):
    def list(self, request):
        client = generate_user_manager_stub()

        # Generate RPC Request
        request_list = acc_typ.UserListRequest()
        request_list.token.CopyFrom(token.token)

        # fetch all users and convert from message to a list of dict
        user_list = [MessageToDict(user, True) for user in client.List(request_list)]

        return Response(user_list, status.HTTP_200_OK)

    def destroy(self, request, pk):
        client = generate_user_manager_stub()

        # Generate RPC Request
        request_destroy = acc_typ.UserDestroyRequest()
        request_destroy.token.CopyFrom(token.token)
        request_destroy.user_id = int(pk)

        try:
            client.Destroy(request_destroy)
        except:
            return Response(
                "Error while removing user", status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response("User Removed", status.HTTP_200_OK)

    def retrieve(self, request, pk):
        client = generate_user_manager_stub()

        # Generate RPC Request
        request_user_retrieve = acc_typ.UserRetrieveRequest()
        request_user_retrieve.user_id = int(pk)
        request_user_retrieve.token.CopyFrom(token.token)

        try:
            result = MessageToDict(client.Retrieve(request_user_retrieve))
        except:
            return Response("User does not exist", status.HTTP_404_NOT_FOUND)

        return Response(result, status.HTTP_200_OK)
