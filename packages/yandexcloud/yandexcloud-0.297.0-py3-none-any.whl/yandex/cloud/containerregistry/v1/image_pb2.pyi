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
import yandex.cloud.containerregistry.v1.blob_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Image(google.protobuf.message.Message):
    """An Image resource. For more information, see [Docker image](/docs/container-registry/concepts/docker-image)."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DIGEST_FIELD_NUMBER: builtins.int
    COMPRESSED_SIZE_FIELD_NUMBER: builtins.int
    CONFIG_FIELD_NUMBER: builtins.int
    LAYERS_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    id: builtins.str
    """Output only. ID of the Docker image."""
    name: builtins.str
    """Name of the Docker image.
    The name is unique within the registry.
    """
    digest: builtins.str
    """Content-addressable identifier of the Docker image."""
    compressed_size: builtins.int
    """Compressed size of the Docker image, specified in bytes."""
    @property
    def config(self) -> yandex.cloud.containerregistry.v1.blob_pb2.Blob:
        """Configuration of the Docker image."""

    @property
    def layers(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.containerregistry.v1.blob_pb2.Blob]:
        """Layers of the Docker image."""

    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Tags of the Docker image.

        Each tag is unique within the repository.
        """

    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Output only. Creation timestamp in [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) text format."""

    def __init__(
        self,
        *,
        id: builtins.str = ...,
        name: builtins.str = ...,
        digest: builtins.str = ...,
        compressed_size: builtins.int = ...,
        config: yandex.cloud.containerregistry.v1.blob_pb2.Blob | None = ...,
        layers: collections.abc.Iterable[yandex.cloud.containerregistry.v1.blob_pb2.Blob] | None = ...,
        tags: collections.abc.Iterable[builtins.str] | None = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["config", b"config", "created_at", b"created_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["compressed_size", b"compressed_size", "config", b"config", "created_at", b"created_at", "digest", b"digest", "id", b"id", "layers", b"layers", "name", b"name", "tags", b"tags"]) -> None: ...

global___Image = Image
