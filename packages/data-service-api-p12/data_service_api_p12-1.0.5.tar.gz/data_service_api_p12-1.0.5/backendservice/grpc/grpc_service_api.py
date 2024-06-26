
import grpc
from google.protobuf import empty_pb2



_EMPTY = empty_pb2.Empty()


class RemoveError(Exception):
    """Raised by the gRPC library to indicate non-OK-status RPC termination."""

    def __init__(self, e: grpc.RpcError):
        self.code = e.code()
        self.message = e.details()


def wrapper_rpc_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except grpc.RpcError as rpc_error:
            raise RemoveError(rpc_error)

    return wrapper


class GrpcChannel:
    def __init__(self, port=49001, host='localhost'):
        addr = f'{host}:{port}'
        self.channel = grpc.insecure_channel(addr)

