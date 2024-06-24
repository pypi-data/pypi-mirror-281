"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class GetConnectionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTION_ID_FIELD_NUMBER: builtins.int
    connection_id: builtins.str
    """ID of the connection to get."""
    def __init__(
        self,
        *,
        connection_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["connection_id", b"connection_id"]) -> None: ...

global___GetConnectionRequest = GetConnectionRequest

@typing.final
class SendToConnectionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _DataType:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _DataTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[SendToConnectionRequest._DataType.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        DATA_TYPE_UNSPECIFIED: SendToConnectionRequest._DataType.ValueType  # 0
        BINARY: SendToConnectionRequest._DataType.ValueType  # 1
        """Binary data."""
        TEXT: SendToConnectionRequest._DataType.ValueType  # 2
        """Text data."""

    class DataType(_DataType, metaclass=_DataTypeEnumTypeWrapper): ...
    DATA_TYPE_UNSPECIFIED: SendToConnectionRequest.DataType.ValueType  # 0
    BINARY: SendToConnectionRequest.DataType.ValueType  # 1
    """Binary data."""
    TEXT: SendToConnectionRequest.DataType.ValueType  # 2
    """Text data."""

    CONNECTION_ID_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    connection_id: builtins.str
    """ID of the connection to which send."""
    data: builtins.bytes
    """Data to send."""
    type: global___SendToConnectionRequest.DataType.ValueType
    """Type of the sending data."""
    def __init__(
        self,
        *,
        connection_id: builtins.str = ...,
        data: builtins.bytes = ...,
        type: global___SendToConnectionRequest.DataType.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["connection_id", b"connection_id", "data", b"data", "type", b"type"]) -> None: ...

global___SendToConnectionRequest = SendToConnectionRequest

@typing.final
class SendToConnectionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___SendToConnectionResponse = SendToConnectionResponse

@typing.final
class DisconnectRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTION_ID_FIELD_NUMBER: builtins.int
    connection_id: builtins.str
    """ID of the connection to disconnect."""
    def __init__(
        self,
        *,
        connection_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["connection_id", b"connection_id"]) -> None: ...

global___DisconnectRequest = DisconnectRequest

@typing.final
class DisconnectResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DisconnectResponse = DisconnectResponse
