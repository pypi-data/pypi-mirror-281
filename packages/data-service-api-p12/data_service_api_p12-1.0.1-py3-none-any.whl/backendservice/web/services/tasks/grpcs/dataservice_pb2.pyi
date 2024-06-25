from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Size_(_message.Message):
    __slots__ = ("width", "height")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    width: float
    height: float
    def __init__(self, width: _Optional[float] = ..., height: _Optional[float] = ...) -> None: ...

class Point_(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class Rect_(_message.Message):
    __slots__ = ("left", "top", "width", "height")
    LEFT_FIELD_NUMBER: _ClassVar[int]
    TOP_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    left: float
    top: float
    width: float
    height: float
    def __init__(self, left: _Optional[float] = ..., top: _Optional[float] = ..., width: _Optional[float] = ..., height: _Optional[float] = ...) -> None: ...

class Polygon_(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[Point_]
    def __init__(self, points: _Optional[_Iterable[_Union[Point_, _Mapping]]] = ...) -> None: ...

class Shape_(_message.Message):
    __slots__ = ("polygon", "box")
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    BOX_FIELD_NUMBER: _ClassVar[int]
    polygon: Polygon_
    box: Rect_
    def __init__(self, polygon: _Optional[_Union[Polygon_, _Mapping]] = ..., box: _Optional[_Union[Rect_, _Mapping]] = ...) -> None: ...

class TaskRequest_(_message.Message):
    __slots__ = ("type", "id", "code")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    type: str
    id: str
    code: str
    def __init__(self, type: _Optional[str] = ..., id: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class AlgData_(_message.Message):
    __slots__ = ("algId", "algParams", "algData")
    ALGID_FIELD_NUMBER: _ClassVar[int]
    ALGPARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGDATA_FIELD_NUMBER: _ClassVar[int]
    algId: str
    algParams: str
    algData: bytes
    def __init__(self, algId: _Optional[str] = ..., algParams: _Optional[str] = ..., algData: _Optional[bytes] = ...) -> None: ...

class Mission_(_message.Message):
    __slots__ = ("missionID", "shape", "algs")
    MISSIONID_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    ALGS_FIELD_NUMBER: _ClassVar[int]
    missionID: str
    shape: Shape_
    algs: _containers.RepeatedCompositeFieldContainer[AlgData_]
    def __init__(self, missionID: _Optional[str] = ..., shape: _Optional[_Union[Shape_, _Mapping]] = ..., algs: _Optional[_Iterable[_Union[AlgData_, _Mapping]]] = ...) -> None: ...

class TaskResponse_(_message.Message):
    __slots__ = ("result", "message", "missions")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MISSIONS_FIELD_NUMBER: _ClassVar[int]
    result: int
    message: str
    missions: _containers.RepeatedCompositeFieldContainer[Mission_]
    def __init__(self, result: _Optional[int] = ..., message: _Optional[str] = ..., missions: _Optional[_Iterable[_Union[Mission_, _Mapping]]] = ...) -> None: ...
