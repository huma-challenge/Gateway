from gateway.grpc_manager.manager import Manager

# The address of gRPC Server on the network
target = "127.0.0.1:50051"
sub_account_manager = Manager(target)
