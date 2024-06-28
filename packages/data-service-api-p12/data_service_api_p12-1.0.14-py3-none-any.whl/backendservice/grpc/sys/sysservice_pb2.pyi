from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JwtRequest_(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class TokenUser_(_message.Message):
    __slots__ = ("exp", "sub", "uid", "roles")
    EXP_FIELD_NUMBER: _ClassVar[int]
    SUB_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    exp: int
    sub: str
    uid: str
    roles: str
    def __init__(self, exp: _Optional[int] = ..., sub: _Optional[str] = ..., uid: _Optional[str] = ..., roles: _Optional[str] = ...) -> None: ...

class JwtResponse_(_message.Message):
    __slots__ = ("status", "message", "details", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: int
    message: str
    details: str
    data: TokenUser_
    def __init__(self, status: _Optional[int] = ..., message: _Optional[str] = ..., details: _Optional[str] = ..., data: _Optional[_Union[TokenUser_, _Mapping]] = ...) -> None: ...
