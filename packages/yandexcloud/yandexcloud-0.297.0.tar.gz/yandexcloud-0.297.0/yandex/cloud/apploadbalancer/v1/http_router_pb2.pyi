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
import yandex.cloud.apploadbalancer.v1.virtual_host_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class HttpRouter(google.protobuf.message.Message):
    """An HTTP router resource.
    For details about the concept, see [documentation](/docs/application-load-balancer/concepts/http-router).
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class LabelsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    FOLDER_ID_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    VIRTUAL_HOSTS_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    ROUTE_OPTIONS_FIELD_NUMBER: builtins.int
    id: builtins.str
    """ID of the router. Generated at creation time."""
    name: builtins.str
    """Name of the router. The name is unique within the folder."""
    description: builtins.str
    """Description of the router."""
    folder_id: builtins.str
    """ID of the folder that the router belongs to."""
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Router labels as `key:value` pairs.
        For details about the concept, see [documentation](/docs/overview/concepts/services#labels).
        """

    @property
    def virtual_hosts(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.apploadbalancer.v1.virtual_host_pb2.VirtualHost]:
        """Virtual hosts that combine routes inside the router.
        For details about the concept, see [documentation](/docs/application-load-balancer/concepts/http-router#virtual-host).

        Only one virtual host with no authority (default match) can be specified.
        """

    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Creation timestamp."""

    @property
    def route_options(self) -> yandex.cloud.apploadbalancer.v1.virtual_host_pb2.RouteOptions: ...
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        folder_id: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        virtual_hosts: collections.abc.Iterable[yandex.cloud.apploadbalancer.v1.virtual_host_pb2.VirtualHost] | None = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        route_options: yandex.cloud.apploadbalancer.v1.virtual_host_pb2.RouteOptions | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["created_at", b"created_at", "route_options", b"route_options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["created_at", b"created_at", "description", b"description", "folder_id", b"folder_id", "id", b"id", "labels", b"labels", "name", b"name", "route_options", b"route_options", "virtual_hosts", b"virtual_hosts"]) -> None: ...

global___HttpRouter = HttpRouter
