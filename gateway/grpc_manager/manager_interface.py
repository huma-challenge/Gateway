from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
import grpc


class ManagerInterface(ABC):
    @abstractmethod
    def create_new_channel(self) -> grpc.Channel:
        ...

    @abstractmethod
    def create_new_client(self, service: grpc):
        ...

    @abstractproperty
    def channel(self) -> grpc.Channel:
        ...
