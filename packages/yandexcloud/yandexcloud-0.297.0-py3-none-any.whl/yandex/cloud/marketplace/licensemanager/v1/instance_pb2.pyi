"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing
import yandex.cloud.marketplace.licensemanager.v1.lock_pb2
import yandex.cloud.marketplace.licensemanager.v1.template_pb2

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Instance(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _State:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _StateEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Instance._State.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        STATE_UNSPECIFIED: Instance._State.ValueType  # 0
        PENDING: Instance._State.ValueType  # 1
        """Subscription created but not active yet."""
        ACTIVE: Instance._State.ValueType  # 2
        """Subscription is active."""
        CANCELLED: Instance._State.ValueType  # 3
        """Subscription canceled. It is still active, but won't be automatically renewed after the end of the current period."""
        EXPIRED: Instance._State.ValueType  # 4
        """Subscription expired."""
        DEPRECATED: Instance._State.ValueType  # 5
        """Subscription deprecated."""
        DELETED: Instance._State.ValueType  # 6
        """Subscription deleted."""

    class State(_State, metaclass=_StateEnumTypeWrapper): ...
    STATE_UNSPECIFIED: Instance.State.ValueType  # 0
    PENDING: Instance.State.ValueType  # 1
    """Subscription created but not active yet."""
    ACTIVE: Instance.State.ValueType  # 2
    """Subscription is active."""
    CANCELLED: Instance.State.ValueType  # 3
    """Subscription canceled. It is still active, but won't be automatically renewed after the end of the current period."""
    EXPIRED: Instance.State.ValueType  # 4
    """Subscription expired."""
    DEPRECATED: Instance.State.ValueType  # 5
    """Subscription deprecated."""
    DELETED: Instance.State.ValueType  # 6
    """Subscription deleted."""

    ID_FIELD_NUMBER: builtins.int
    CLOUD_ID_FIELD_NUMBER: builtins.int
    FOLDER_ID_FIELD_NUMBER: builtins.int
    TEMPLATE_ID_FIELD_NUMBER: builtins.int
    TEMPLATE_VERSION_ID_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    START_TIME_FIELD_NUMBER: builtins.int
    END_TIME_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    UPDATED_AT_FIELD_NUMBER: builtins.int
    STATE_FIELD_NUMBER: builtins.int
    LOCKS_FIELD_NUMBER: builtins.int
    LICENSE_TEMPLATE_FIELD_NUMBER: builtins.int
    id: builtins.str
    """ID of the subscription instance."""
    cloud_id: builtins.str
    """ID of the cloud that the subscription instance belongs to."""
    folder_id: builtins.str
    """ID of the folder that the subscription instance belongs to."""
    template_id: builtins.str
    """ID of the subscription template that was used to create subscription instance."""
    template_version_id: builtins.str
    """ID of the version of subscription template."""
    description: builtins.str
    """Description of the subscription instance."""
    state: global___Instance.State.ValueType
    """Subscription state."""
    @property
    def start_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Timestamp of the start of the subscription."""

    @property
    def end_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Timestamp of the end of the subscription."""

    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Creation timestamp."""

    @property
    def updated_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Update timestamp."""

    @property
    def locks(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.marketplace.licensemanager.v1.lock_pb2.Lock]:
        """List of subscription locks."""

    @property
    def license_template(self) -> yandex.cloud.marketplace.licensemanager.v1.template_pb2.Template:
        """Subscription template."""

    def __init__(
        self,
        *,
        id: builtins.str = ...,
        cloud_id: builtins.str = ...,
        folder_id: builtins.str = ...,
        template_id: builtins.str = ...,
        template_version_id: builtins.str = ...,
        description: builtins.str = ...,
        start_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        end_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        updated_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        state: global___Instance.State.ValueType = ...,
        locks: collections.abc.Iterable[yandex.cloud.marketplace.licensemanager.v1.lock_pb2.Lock] | None = ...,
        license_template: yandex.cloud.marketplace.licensemanager.v1.template_pb2.Template | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["created_at", b"created_at", "end_time", b"end_time", "license_template", b"license_template", "start_time", b"start_time", "updated_at", b"updated_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["cloud_id", b"cloud_id", "created_at", b"created_at", "description", b"description", "end_time", b"end_time", "folder_id", b"folder_id", "id", b"id", "license_template", b"license_template", "locks", b"locks", "start_time", b"start_time", "state", b"state", "template_id", b"template_id", "template_version_id", b"template_version_id", "updated_at", b"updated_at"]) -> None: ...

global___Instance = Instance
