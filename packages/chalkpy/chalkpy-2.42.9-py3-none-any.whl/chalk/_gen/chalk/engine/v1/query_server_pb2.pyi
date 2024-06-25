from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.common.v1 import compilation_options_pb2 as _compilation_options_pb2
from chalk._gen.chalk.common.v1 import online_query_pb2 as _online_query_pb2
from chalk._gen.chalk.plan.v1 import plan_pb2 as _plan_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class PingRequest(_message.Message):
    __slots__ = ("num",)
    NUM_FIELD_NUMBER: _ClassVar[int]
    num: int
    def __init__(self, num: _Optional[int] = ...) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ("num",)
    NUM_FIELD_NUMBER: _ClassVar[int]
    num: int
    def __init__(self, num: _Optional[int] = ...) -> None: ...

class QueryFromPlanRequest(_message.Message):
    __slots__ = ("plan", "compilation_options", "query_id")
    PLAN_FIELD_NUMBER: _ClassVar[int]
    COMPILATION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    plan: _plan_pb2.LogicalTableNode
    compilation_options: _compilation_options_pb2.CompilationOptions
    query_id: str
    def __init__(
        self,
        plan: _Optional[_Union[_plan_pb2.LogicalTableNode, _Mapping]] = ...,
        compilation_options: _Optional[_Union[_compilation_options_pb2.CompilationOptions, _Mapping]] = ...,
        query_id: _Optional[str] = ...,
    ) -> None: ...

class QueryFromPlanResponse(_message.Message):
    __slots__ = ("data", "errors")
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[QueryFromPlanTable]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        data: _Optional[_Iterable[_Union[QueryFromPlanTable, _Mapping]]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class QueryFromPlanTable(_message.Message):
    __slots__ = ("feather",)
    FEATHER_FIELD_NUMBER: _ClassVar[int]
    feather: bytes
    def __init__(self, feather: _Optional[bytes] = ...) -> None: ...
