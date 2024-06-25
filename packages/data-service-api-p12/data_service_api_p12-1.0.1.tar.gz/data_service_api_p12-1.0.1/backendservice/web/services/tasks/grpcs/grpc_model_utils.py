from typing import List, Union, Dict

from backendservice.grpc.grpcutils import value_or_empty, bytes_or_empty
from backendservice.util.exceptions import ErrorException, ErrorCode
from backendservice.web.services.tasks.grpcs.dataservice_pb2 import  Mission_,   TaskResponse_, TaskRequest_, Shape_, Point_, AlgData_
from backendservice.web.services.tasks.grpcs.grpc_models import Mission, \
    TaskResponse, TaskRequest, AlgData, Rect2, Point2


class pb2_to_local:
    """

    # 将 GRPC 数据转换为 Python Models

    """

    ###################################


    @staticmethod
    def to_TaskRequest (prop: TaskRequest_ ) -> TaskRequest :
        out = TaskRequest( prop.id , prop.code , prop.type)
        return out



    #################################

    @staticmethod
    def to_Shape(shape: Shape_) -> Union[Rect2, List[Point2]]:

        if shape.HasField("box"):
            b = Rect2()
            b.top = shape.box.top
            b.left = shape.box.left
            b.width = shape.box.width
            b.height = shape.box.height
            return b

        if shape.HasField("polygon"):
            c: List[Point2] = []
            for one in shape.polygon.points:
                c.append(Point2(one.x, one.y))
            return c

        raise ErrorException(ErrorCode.invalid_argument, f"Unknown type - {type(shape)} , {shape.ListFields()}")


    #####################################################

    @staticmethod
    def to_AlgData(a: AlgData_) -> AlgData:
        b = AlgData()
        b.alg_id = a.algId
        b.alg_data = a.algData
        b.alg_params = a.algParams

        return b

    @staticmethod
    def to_Mission(m: Mission_) -> Mission:
        mission_id = m.missionID
        o = Mission(mission_id)
        o.shape = pb2_to_local.to_Shape(m.shape)
        for one in m.algs:
            alg = pb2_to_local.to_AlgData(one)
            o.add_alg(alg)
        return o





    @staticmethod
    def to_TaskResponse (p: TaskResponse_) -> TaskResponse :
        req = TaskResponse (  result=p.result, message=p.message)
        for mission in p.missions:
            nm = pb2_to_local.to_Mission(mission)
            req.missions.append(nm)
        return req
#####################################################################################################################


class local_to_pb2:
    """

    # 将 Python Models  数据转换为 GRPC

    """

    @staticmethod
    def to_TaskRequest_(prop: TaskRequest ) -> TaskRequest_:
        out = TaskRequest_(id=value_or_empty(prop.id_), code=value_or_empty(prop.code), type=value_or_empty(prop.type) )
        return out


    @staticmethod
    def to_Shape_(shape) -> Shape_:

        if isinstance(shape, Rect2):
            a = Shape_()
            b: Rect2 = shape
            a.box.top = b.top
            a.box.left = b.left
            a.box.width = b.width
            a.box.height = b.height
            return a

        if isinstance(shape, list):
            # should be List[Point]
            a = Shape_()
            b: List[Point2] = shape
            for one in b:
                a.polygon.points.append(Point_(x=one.x, y=one.y))

        raise ErrorException(ErrorCode.invalid_argument, f"Unknown type - {type(shape)} , {shape}")

    @staticmethod
    def to_AlgData_(a: AlgData) -> AlgData_:

        c = AlgData_(algId=value_or_empty(a.alg_id), algData=bytes_or_empty(a.alg_data),
                        algParams=value_or_empty(a.alg_params))
        return c

    @staticmethod
    def to_Mission_(m: Mission) -> Mission_:
        shape = local_to_pb2.to_Shape_(m.shape)

        mission = Mission_(missionID=value_or_empty(m.mission_id), shape=shape)

        for one in m.algs:
            alg = local_to_pb2.to_AlgData_(one)
            mission.algs.append(alg)

        return mission




    @staticmethod
    def to_TaskResponse_(p: TaskResponse) -> TaskResponse_:
        req = TaskResponse_(  result=p.result, message=value_or_empty(p.message))
        for mission in p.missions:
            nm = local_to_pb2.to_Mission_(mission)
            req.missions.append(nm)
        return req
