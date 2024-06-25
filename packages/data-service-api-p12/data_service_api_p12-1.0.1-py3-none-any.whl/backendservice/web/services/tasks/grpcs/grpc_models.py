from typing import List, Union, Dict

from backendservice.util.exceptions import ErrorException, ErrorCode
from backendservice.util.jsonencoder import json_to_dict, read_dict_val


class TaskRequest:
    def __init__(self, id_: str = "", code : str = "", type: str = ""):
        self.id_ = id_
        self.type = type
        self.code = code


class Rect2:
    def __init__(self, left=0, top=0, width=0, height=0):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def __str__(self):
        return f'left:{self.left} ,top:{self.top} ,width:{self.width} ,height:{self.height} '


class Point2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x:{self.x} ,y:{self.y}'


class AlgData:
    def __init__(self):
        self.alg_id = ""
        self.alg_params = ""
        self.alg_data: Union[bytes, None] = None


class Mission:

    def __init__(self, mission_id: str):
        self.mission_id = mission_id
        self.shape: Union[Rect2, List[Point2], None] = None
        self.algs: List[AlgData] = []

    def set_shape_rect(self, rect: Rect2):
        self.shape = rect

    def set_shape_points(self, pts: List[Point2]):
        self.shape = pts

    def add_alg(self, alg: AlgData):
        self.algs.append(alg)


class TaskResponse:
    def __init__(self, result: int, message: str):
        self.result = result
        self.message = message
        self.missions: List[Mission] = []

    def add(self, ad: Mission):
        self.missions.append(ad)






def to_rect2(shape: str) -> Rect2:
    js = json_to_dict(shape)
    left = read_dict_val(js, "left")
    top = read_dict_val(js, "top")
    width = read_dict_val(js, "width")
    height = read_dict_val(js, "height")
    return Rect2(left, top, width, height)


def to_points2(shape: str) -> List[Point2]:
    ps_ = []
    ps = json_to_dict(shape)

    for p in ps:
        x = read_dict_val(p, "x")
        y = read_dict_val(p, "y")
        ps_.append(Point2(x, y))

    return ps_


def to_shape(shape: str, shape_type: str):
    if shape_type == "rect":
        return to_rect2(shape)
    elif shape_type == "polygon":
        return to_points2(shape)
    else:
        raise ErrorException(ErrorCode.invalid_argument, f"not support shape_type : {shape_type} ")
