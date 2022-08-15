import grpc


def create_new_channel(address) -> grpc.Channel:
    channel = grpc.insecure_channel()
    return channel


def create_new_client(channel: grpc.Channel, service: grpc):
    client = service(channel)
    return client
