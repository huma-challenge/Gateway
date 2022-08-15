from typing import List
import grpc
from gateway.grpc_manager.manager_interface import ManagerInterface


class BaseManager(ManagerInterface):
    """Singleton base manager based on the target.
    this base manager can reuse channels based on
    the address of the target server, and return it,
    if there are no channels create a new channel based on

    Args:
        target (str): the address of target server
    """

    # map of created channels with same target for reuse channels
    channels: List[grpc.Channel] = {}
    # address of target server
    target: str
    channel: grpc.Channel

    def __init__(self, target: str = "") -> None:
        self.target = target
        self.create_new_channel()

    def __new__(cls, target, *args, **kwargs):

        # return instance of the channel with same target
        # to avoid recreate new channel with same target
        if target in cls.channels:
            return cls.channels[target]

        # Create new channel based on target and saved it
        manager = super(BaseManager, cls).__new__(cls, *args, **kwargs)
        cls.channels[target] = manager

        return manager




def create_new_client(channel: grpc.Channel, service: grpc):
    client = service(channel)
    return client
