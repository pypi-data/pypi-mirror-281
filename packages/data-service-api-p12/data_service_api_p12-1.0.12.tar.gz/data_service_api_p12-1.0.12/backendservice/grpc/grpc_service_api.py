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

        # options = [('grpc.max_send_message_length', 20 * 1024 * 1024),
        #            ('grpc.max_receive_message_length', 20 * 1024 * 1024),
        #            ('grpc.enable_retries', 1),
        #            ('grpc.service_config',
        #             '{ "hedgingPolicy":{ "maxAttempts": 4, "hedgingDelay": "0.5s", "nonFatalStatusCodes":[ "UNAVAILABLE", "INTERNAL", "ABORTED" ] } }')]
        #
        # self.channel = grpc.insecure_channel(addr, options=options)
        self.channel = grpc.insecure_channel(addr)