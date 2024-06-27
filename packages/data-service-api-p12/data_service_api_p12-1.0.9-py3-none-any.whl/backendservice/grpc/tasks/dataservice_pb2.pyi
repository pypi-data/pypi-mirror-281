from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskRequest_(_message.Message):
    __slots__ = ("objType", "objId", "code")
    OBJTYPE_FIELD_NUMBER: _ClassVar[int]
    OBJID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    objType: str
    objId: str
    code: str
    def __init__(self, objType: _Optional[str] = ..., objId: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class PageMissionAlg_(_message.Message):
    __slots__ = ("missionId", "algId", "algConfig", "algData")
    MISSIONID_FIELD_NUMBER: _ClassVar[int]
    ALGID_FIELD_NUMBER: _ClassVar[int]
    ALGCONFIG_FIELD_NUMBER: _ClassVar[int]
    ALGDATA_FIELD_NUMBER: _ClassVar[int]
    missionId: str
    algId: str
    algConfig: str
    algData: bytes
    def __init__(self, missionId: _Optional[str] = ..., algId: _Optional[str] = ..., algConfig: _Optional[str] = ..., algData: _Optional[bytes] = ...) -> None: ...

class PageMission_(_message.Message):
    __slots__ = ("missionId", "shape", "shape_type")
    MISSIONID_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_TYPE_FIELD_NUMBER: _ClassVar[int]
    missionId: str
    shape: str
    shape_type: str
    def __init__(self, missionId: _Optional[str] = ..., shape: _Optional[str] = ..., shape_type: _Optional[str] = ...) -> None: ...

class PageObj_(_message.Message):
    __slots__ = ("code", "camera", "missions", "algs")
    CODE_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    MISSIONS_FIELD_NUMBER: _ClassVar[int]
    ALGS_FIELD_NUMBER: _ClassVar[int]
    code: str
    camera: str
    missions: _containers.RepeatedCompositeFieldContainer[PageMission_]
    algs: _containers.RepeatedCompositeFieldContainer[PageMissionAlg_]
    def __init__(self, code: _Optional[str] = ..., camera: _Optional[str] = ..., missions: _Optional[_Iterable[_Union[PageMission_, _Mapping]]] = ..., algs: _Optional[_Iterable[_Union[PageMissionAlg_, _Mapping]]] = ...) -> None: ...

class PageObjResult_(_message.Message):
    __slots__ = ("result", "message", "data")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    result: int
    message: str
    data: PageObj_
    def __init__(self, result: _Optional[int] = ..., message: _Optional[str] = ..., data: _Optional[_Union[PageObj_, _Mapping]] = ...) -> None: ...
