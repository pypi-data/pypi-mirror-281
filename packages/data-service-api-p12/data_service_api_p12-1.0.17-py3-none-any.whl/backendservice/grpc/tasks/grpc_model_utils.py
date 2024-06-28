from backendservice.grpc.grpcutils import value_or_empty, bytes_or_empty, value_or_zero

from backendservice.grpc.tasks.dataservice_pb2 import TaskRequest_, \
    PageObjResult_, PageObj_, PageMission_, PageMissionAlg_, DetectAudit_, DetectResultResponse_
from backendservice.grpc.tasks.grpc_models import TaskRequest, PageObj, PageMissionAlg, PageMission, DetectAudit
from backendservice.util.exceptions import ErrorCode


class pb2_to_local:
    """

    # 将 GRPC 数据转换为 Python Models

    """

    ###################################

    @staticmethod
    def to_TaskRequest(prop: TaskRequest_) -> TaskRequest:
        out = TaskRequest(prop.objId, prop.code, prop.objType)
        return out

    #################################

    @staticmethod
    def to_PageObj(page: PageObj_) -> PageObj:

        out = PageObj(task_id= page.taskId, template_id= page.templateId,
                      code=page.code, camera=page.camera)
        out.missions = []
        out.mission_algs = []
        out.task_id = page.taskId
        out.template_id = page.templateId
        for mm in page.missions:
            mission = PageMission(mission_id=value_or_empty(mm.missionId), shape=value_or_empty(mm.shape),
                                  shape_type=value_or_empty(mm.shape_type))
            out.missions.append(mission)

        for alg in page.algs:
            aa = PageMissionAlg(mission_id=value_or_empty(alg.missionId),
                                alg_id=value_or_empty(alg.algId),
                                alg_config=value_or_empty(alg.algConfig),
                                alg_data=bytes_or_empty(alg.algData))
            out.mission_algs.append(aa)

        return out

    ##################################################

    @staticmethod
    def to_DetectAudit (da: DetectAudit_) -> DetectAudit:
        out = DetectAudit(user=value_or_empty(da.user), user_id=value_or_zero(da.user_id),
                          image_uuid=value_or_empty(da.image_uuid),
                          begin=value_or_empty(da.begin), end=value_or_empty(da.end),
                          times=value_or_zero(da.times),
                          reason=value_or_zero(da.reason),
                          product_code=value_or_empty(da.product_code),
                          task_id=value_or_zero(da.taskId), template_id=value_or_zero(da.templateId))
        return out





#####################################################################################################################


class local_to_pb2:
    """

    # 将 Python Models  数据转换为 GRPC

    """

    @staticmethod
    def to_TaskRequest_(prop: TaskRequest) -> TaskRequest_:
        out = TaskRequest_(objId=value_or_empty(prop.id_), code=value_or_empty(prop.code),
                           objType=value_or_empty(prop.type_))
        return out

    @staticmethod
    def to_PageObj_(page: PageObj) -> PageObj_:

        out = PageObj_(code=value_or_empty(page.code), camera=value_or_empty(page.camera),
                       templateId=value_or_zero(page.template_id), taskId=value_or_zero(page.task_id))

        for mm in page.missions:
            mission = PageMission_(missionId=value_or_empty(mm.mission_id), shape=value_or_empty(mm.shape),
                                   shape_type=value_or_empty(mm.shape_type))
            out.missions.append(mission)

        for alg in page.mission_algs:
            aa = PageMissionAlg_(missionId=value_or_empty(alg.mission_id),
                                 algId=value_or_empty(alg.alg_id),
                                 algConfig=value_or_empty(alg.alg_config),
                                 algData=bytes_or_empty(alg.alg_data))
            out.algs.append(aa)

        return out

    @staticmethod
    def to_PageObjResult_(status: int, message: str, details: str,
                          p: PageObj = None) -> PageObjResult_:

        if p is not None:
            data = local_to_pb2.to_PageObj_(p)
            req = PageObjResult_(status=status, message=value_or_empty(message), details=value_or_empty(details),
                                 data=data)
        else:
            req = PageObjResult_(status=status, message=value_or_empty(message), details=value_or_empty(details))
        return req

    #####################################################

    @staticmethod
    def to_DetectAudit_(da: DetectAudit) -> DetectAudit_:
        out = DetectAudit_(user=value_or_empty(da.user), user_id=value_or_zero(da.user_id),
                           image_uuid=value_or_empty(da.image_uuid),
                           begin=value_or_empty(da.begin), end=value_or_empty(da.end),
                           times=value_or_zero(da.times),
                           reason=value_or_zero(da.reason),
                           product_code=value_or_empty(da.product_code),
                           taskId=value_or_zero(da.task_id), templateId=value_or_zero(da.template_id))
        return out



    @staticmethod
    def to_DetectResultResponse_(status: int = ErrorCode.ok, message: str = "", details: str = ""
                      ) -> DetectResultResponse_:

        resp = DetectResultResponse_(status=status, message=value_or_empty(message), details=value_or_empty(details))
        return resp