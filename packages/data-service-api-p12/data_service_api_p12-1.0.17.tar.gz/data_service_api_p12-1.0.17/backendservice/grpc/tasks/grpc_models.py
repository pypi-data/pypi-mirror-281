from typing import List


class TaskRequest:
    def __init__(self, id_: str = "", code: str = "", type_: str = ""):
        self.id_ = id_
        self.type_ = type_
        self.code = code


class PageMission:
    def __init__(self, mission_id: str = "", shape_type: str = "", shape: str = ""):
        self.shape_type = shape_type
        self.shape = shape
        self.mission_id = mission_id


class PageMissionAlg:

    def __init__(self, mission_id: str = "", alg_id: str = "", alg_config: str = "", alg_data: bytes = None):
        self.alg_id = alg_id
        self.alg_config = alg_config
        self.alg_data = alg_data
        self.mission_id = mission_id


class PageObj:

    def __init__(self, task_id: int, template_id: int, code: str = "", camera: str = ""):
        self.task_id = task_id
        self.template_id = template_id
        self.code = code
        self.camera = camera
        self.missions: List[PageMission] = []
        self.mission_algs: List[PageMissionAlg] = []


class DetectAudit:

    def __init__(self, user:str ="" , user_id:int =0,
                 image_uuid:str ="",
                 begin: str ="",
                 end: str ="",
                 times: int =0,
                 reason: int =0,
                 task_id: int =0, template_id: int =0, product_code: str = "" ):
        self.user  = user
        self.user_id = user_id
        self.image_uuid = image_uuid
        self.begin = begin
        self.end = end
        self.times = times
        self.reason = reason
        self.task_id = task_id
        self.template_id = template_id
        self.product_code = product_code


