"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class ResourcePreset(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    CORES_FIELD_NUMBER: builtins.int
    MEMORY_FIELD_NUMBER: builtins.int
    id: builtins.str
    cores: builtins.int
    memory: builtins.int
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        cores: builtins.int = ...,
        memory: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cores", b"cores", "id", b"id", "memory", b"memory"]) -> None: ...

global___ResourcePreset = ResourcePreset
