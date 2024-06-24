"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Backup(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    FOLDER_ID_FIELD_NUMBER: builtins.int
    SOURCE_CLUSTER_ID_FIELD_NUMBER: builtins.int
    STARTED_AT_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    INDICES_FIELD_NUMBER: builtins.int
    OPENSEARCH_VERSION_FIELD_NUMBER: builtins.int
    SIZE_BYTES_FIELD_NUMBER: builtins.int
    INDICES_TOTAL_FIELD_NUMBER: builtins.int
    id: builtins.str
    """Required. ID of the backup."""
    folder_id: builtins.str
    """ID of the folder that the backup belongs to."""
    source_cluster_id: builtins.str
    """ID of the OpenSearch cluster that the backup was created for."""
    opensearch_version: builtins.str
    """OpenSearch version used to create the backup."""
    size_bytes: builtins.int
    """Size of the backup in bytes."""
    indices_total: builtins.int
    """The number of indices in the backup."""
    @property
    def started_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Time when the backup operation was started."""

    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Time when the backup operation was completed."""

    @property
    def indices(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Names of indices in the backup."""

    def __init__(
        self,
        *,
        id: builtins.str = ...,
        folder_id: builtins.str = ...,
        source_cluster_id: builtins.str = ...,
        started_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        indices: collections.abc.Iterable[builtins.str] | None = ...,
        opensearch_version: builtins.str = ...,
        size_bytes: builtins.int = ...,
        indices_total: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["created_at", b"created_at", "started_at", b"started_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["created_at", b"created_at", "folder_id", b"folder_id", "id", b"id", "indices", b"indices", "indices_total", b"indices_total", "opensearch_version", b"opensearch_version", "size_bytes", b"size_bytes", "source_cluster_id", b"source_cluster_id", "started_at", b"started_at"]) -> None: ...

global___Backup = Backup
