from typing import List


class TaskRequest:
    def __init__(self, id_: str = "", code: str = "", type_: str = ""):
        self.id_ = id_
        self.type_ = type_
        self.code = code


class  PageMission:
    def __init__(self, mission_id: str = "", shape_type: str = "", shape: str = ""):
        self.shape_type = shape_type
        self.shape = shape
        self.mission_id = mission_id


class  PageMissionAlg:

    def __init__(self, mission_id: str = "", alg_id: str = "", alg_config: str = "", alg_data: bytes = None):
        self.alg_id = alg_id
        self.alg_config = alg_config
        self.alg_data = alg_data
        self.mission_id = mission_id


class  PageObj:

    def __init__(self, code: str = "", camera: str = ""):
        self.code = code
        self.camera = camera
        self.missions: List[ PageMission] = []
        self.mission_algs: List[ PageMissionAlg] = []
