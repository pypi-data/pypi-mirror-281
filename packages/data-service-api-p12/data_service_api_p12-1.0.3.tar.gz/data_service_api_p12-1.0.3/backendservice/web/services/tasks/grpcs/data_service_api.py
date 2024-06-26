from backendservice.grpc.grpc_service_api import GrpcChannel, wrapper_rpc_error

from backendservice.util.exceptions import ErrorCode, ErrorException

from backendservice.web.services.tasks.grpcs.dataservice_pb2_grpc import DataServiceStub
from backendservice.web.services.tasks.grpcs.grpc_model_utils import local_to_pb2, pb2_to_local
from backendservice.web.services.tasks.grpcs.grpc_models import TaskRequest, PageObj


class DataServiceApi:

    def __init__(self, channel: GrpcChannel):
        self._stub = DataServiceStub(channel.channel)
        pass

    @wrapper_rpc_error
    def GetTask(self, id_: str, code: str, type: str = "") -> PageObj:
        req = local_to_pb2.to_TaskRequest_(TaskRequest(id_, code, type))
        resp = self._stub.GetTask(req)

        if resp.result != ErrorCode.ok:
            raise ErrorException(resp.result, resp.message)
        return pb2_to_local.to_PageObj(resp.data)


def create_data_api(host, port) -> DataServiceApi:
    c = GrpcChannel(host=host, port=port)
    return DataServiceApi(c)
