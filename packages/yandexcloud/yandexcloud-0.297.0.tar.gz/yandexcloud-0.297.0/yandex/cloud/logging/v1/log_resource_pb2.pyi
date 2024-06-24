"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class LogEntryResource(google.protobuf.message.Message):
    """Log entry resource specification.

    May be used either by services and by user.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TYPE_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    type: builtins.str
    """Resource type, i.e., `serverless.function`"""
    id: builtins.str
    """Resource ID, i.e., ID of the function producing logs."""
    def __init__(
        self,
        *,
        type: builtins.str = ...,
        id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["id", b"id", "type", b"type"]) -> None: ...

global___LogEntryResource = LogEntryResource

@typing.final
class LogGroupResource(google.protobuf.message.Message):
    """Log group resource."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TYPE_FIELD_NUMBER: builtins.int
    IDS_FIELD_NUMBER: builtins.int
    type: builtins.str
    """Resource type.

    Collected from log entries inside log group.
    """
    @property
    def ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """List of resource IDs with the same resource type."""

    def __init__(
        self,
        *,
        type: builtins.str = ...,
        ids: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["ids", b"ids", "type", b"type"]) -> None: ...

global___LogGroupResource = LogGroupResource
