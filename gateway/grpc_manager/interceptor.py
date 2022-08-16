from google.protobuf.json_format import MessageToDict
import logging
import grpc

logger = logging.Logger("interceptor")

from grpc_interceptor import ClientCallDetails, ClientInterceptor


class LoggerInterceptor(ClientInterceptor):
    def intercept(
        self,
        method,
        request_or_iterator,
        call_details: grpc.ClientCallDetails,
    ):

        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            [("authorization", "Bearer mysecrettoken")],
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        msg = {
            "url": call_details.method,
            "request": request_or_iterator,
        }
        logger.info(msg)

        return method(request_or_iterator, new_details)


# class LoggerInterceptor(ServerInterceptor):
#     def intercept(
#         self,
#         method,
#         request,
#         context: grpc.ServicerContext,
#         method_name: str,
#     ):
#         print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
#         try:
#             result = method(request, context)

#             msg = {
#                 "method": method_name,
#                 "reqeust": MessageToDict(request),
#             }
#             # logger.info(msg)

#             return result
#         except GrpcException as e:
#             msg = {
#                 "method": method_name,
#                 "status_code": e.status_code,
#                 "reqeust": MessageToDict(request),
#                 "details": e.details,
#             }
#             # logger.error(msg)

#             # context.set_code(e.status_code)
#             # context.set_details(e.details)
#             # raise
