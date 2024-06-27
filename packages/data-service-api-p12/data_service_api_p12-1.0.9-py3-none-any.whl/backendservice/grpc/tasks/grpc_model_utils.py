from backendservice.grpc.grpcutils import value_or_empty, bytes_or_empty

from backendservice.grpc.tasks.dataservice_pb2 import TaskRequest_, \
     PageObjResult_, PageObj_, PageMission_, PageMissionAlg_
from backendservice.grpc.tasks.grpc_models import TaskRequest, PageObj, PageMissionAlg, PageMission


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

        out = PageObj(code=value_or_empty(page.code), camera=value_or_empty(page.camera))
        out.missions = []
        out.mission_algs = []
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


#####################################################################################################################


class local_to_pb2:
    """

    # 将 Python Models  数据转换为 GRPC

    """

    @staticmethod
    def to_TaskRequest_(prop: TaskRequest) -> TaskRequest_:
        out = TaskRequest_(objId=value_or_empty(prop.id_), code=value_or_empty(prop.code), objType=value_or_empty(prop.type_))
        return out

    @staticmethod
    def to_PageObj_(page: PageObj) -> PageObj_:

        out = PageObj_(code=value_or_empty(page.code), camera=value_or_empty(page.camera))

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
    def to_PageObjResult_(result: int, message: str,
                          p: PageObj = None) -> PageObjResult_:

        if p is not None:
            data = local_to_pb2.to_PageObj_(p)
            req = PageObjResult_(result=result, message=value_or_empty(message), data=data)
        else:
            req = PageObjResult_(result=result, message=value_or_empty(message))
        return req
