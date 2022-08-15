from gateway.grpc_manager.manager import Manager

import environ

# Define and loads env var files
env = environ.Env()

# The address of gRPC Server on the network
target = env("account_manager", default="127.0.0.1:50051")


def get_grcp_manager():
    return Manager(target)
