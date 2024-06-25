from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompilationOptions(_message.Message):
    __slots__ = ("acero", "velox")
    ACERO_FIELD_NUMBER: _ClassVar[int]
    VELOX_FIELD_NUMBER: _ClassVar[int]
    acero: AceroCompilationOptions
    velox: VeloxCompilationOptions
    def __init__(
        self,
        acero: _Optional[_Union[AceroCompilationOptions, _Mapping]] = ...,
        velox: _Optional[_Union[VeloxCompilationOptions, _Mapping]] = ...,
    ) -> None: ...

class AceroCompilationOptions(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class VeloxCompilationOptions(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
