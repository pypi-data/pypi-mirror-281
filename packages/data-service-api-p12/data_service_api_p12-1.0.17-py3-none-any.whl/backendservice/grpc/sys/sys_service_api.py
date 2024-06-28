from backendservice.grpc.grpc_service_api import GrpcChannel, wrapper_rpc_error
from backendservice.grpc.grpcutils import value_or_empty
from backendservice.grpc.sys.grpc_sys_model_utils import TokenUser2, pb2_to_local
from backendservice.grpc.sys.sysservice_pb2 import JwtRequest_
from backendservice.grpc.sys.sysservice_pb2_grpc import SystemServiceStub

from backendservice.util.exceptions import ErrorCode, ErrorException, ErrorDetailException


class SysServiceApi:

    def __init__(self, channel: GrpcChannel):
        self._stub = SystemServiceStub(channel.channel)
        pass

    @wrapper_rpc_error
    def VerifyJwt(self, token: str) -> TokenUser2:
        req = JwtRequest_(token=value_or_empty(token))
        resp = self._stub.VerifyJwt(req)
        if resp.status != ErrorCode.ok:
            raise ErrorDetailException(code=resp.status, message=resp.message,details=resp.details)
        return pb2_to_local.to_TokenUser2(resp.data)


def create_sys_api(host:str, port:int ) -> SysServiceApi:
    c = GrpcChannel(port=port,host=host)
    return SysServiceApi(c)
