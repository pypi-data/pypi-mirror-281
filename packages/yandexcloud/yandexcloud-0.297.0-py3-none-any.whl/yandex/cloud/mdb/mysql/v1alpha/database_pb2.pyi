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
class Database(google.protobuf.message.Message):
    """A MySQL database. For more information, see the [documentation](/docs/managed-mysql/concepts)."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    CLUSTER_ID_FIELD_NUMBER: builtins.int
    name: builtins.str
    """Name of the database."""
    cluster_id: builtins.str
    """ID of the MySQL cluster that the database belongs to."""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        cluster_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cluster_id", b"cluster_id", "name", b"name"]) -> None: ...

global___Database = Database

@typing.final
class DatabaseSpec(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    """Name of the MySQL database."""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["name", b"name"]) -> None: ...

global___DatabaseSpec = DatabaseSpec
