from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogicalTableNode(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: ValuesNode
    def __init__(self, values: _Optional[_Union[ValuesNode, _Mapping]] = ...) -> None: ...

class ValuesNode(_message.Message):
    __slots__ = ("feather",)
    FEATHER_FIELD_NUMBER: _ClassVar[int]
    feather: bytes
    def __init__(self, feather: _Optional[bytes] = ...) -> None: ...
