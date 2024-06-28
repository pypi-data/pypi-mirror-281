from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectAudit_(_message.Message):
    __slots__ = ("user", "user_id", "image_uuid", "begin", "end", "times", "reason", "product_code", "taskId", "templateId")
    USER_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    IMAGE_UUID_FIELD_NUMBER: _ClassVar[int]
    BEGIN_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    TIMES_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_CODE_FIELD_NUMBER: _ClassVar[int]
    TASKID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATEID_FIELD_NUMBER: _ClassVar[int]
    user: str
    user_id: int
    image_uuid: str
    begin: str
    end: str
    times: int
    reason: int
    product_code: str
    taskId: int
    templateId: int
    def __init__(self, user: _Optional[str] = ..., user_id: _Optional[int] = ..., image_uuid: _Optional[str] = ..., begin: _Optional[str] = ..., end: _Optional[str] = ..., times: _Optional[int] = ..., reason: _Optional[int] = ..., product_code: _Optional[str] = ..., taskId: _Optional[int] = ..., templateId: _Optional[int] = ...) -> None: ...

class DetectResultResponse_(_message.Message):
    __slots__ = ("status", "message", "details")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    status: int
    message: str
    details: str
    def __init__(self, status: _Optional[int] = ..., message: _Optional[str] = ..., details: _Optional[str] = ...) -> None: ...

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
    __slots__ = ("code", "camera", "missions", "algs", "taskId", "templateId")
    CODE_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    MISSIONS_FIELD_NUMBER: _ClassVar[int]
    ALGS_FIELD_NUMBER: _ClassVar[int]
    TASKID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATEID_FIELD_NUMBER: _ClassVar[int]
    code: str
    camera: str
    missions: _containers.RepeatedCompositeFieldContainer[PageMission_]
    algs: _containers.RepeatedCompositeFieldContainer[PageMissionAlg_]
    taskId: int
    templateId: int
    def __init__(self, code: _Optional[str] = ..., camera: _Optional[str] = ..., missions: _Optional[_Iterable[_Union[PageMission_, _Mapping]]] = ..., algs: _Optional[_Iterable[_Union[PageMissionAlg_, _Mapping]]] = ..., taskId: _Optional[int] = ..., templateId: _Optional[int] = ...) -> None: ...

class PageObjResult_(_message.Message):
    __slots__ = ("status", "message", "details", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: int
    message: str
    details: str
    data: PageObj_
    def __init__(self, status: _Optional[int] = ..., message: _Optional[str] = ..., details: _Optional[str] = ..., data: _Optional[_Union[PageObj_, _Mapping]] = ...) -> None: ...
