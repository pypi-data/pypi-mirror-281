"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.duration_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing
import yandex.cloud.logging.v1.log_entry_pb2

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Container(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Status:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _StatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Container._Status.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        STATUS_UNSPECIFIED: Container._Status.ValueType  # 0
        CREATING: Container._Status.ValueType  # 1
        """Container is being created."""
        ACTIVE: Container._Status.ValueType  # 2
        """Container is ready for use."""
        DELETING: Container._Status.ValueType  # 3
        """Container is being deleted."""
        ERROR: Container._Status.ValueType  # 4
        """Container failed. The only allowed action is delete."""

    class Status(_Status, metaclass=_StatusEnumTypeWrapper): ...
    STATUS_UNSPECIFIED: Container.Status.ValueType  # 0
    CREATING: Container.Status.ValueType  # 1
    """Container is being created."""
    ACTIVE: Container.Status.ValueType  # 2
    """Container is ready for use."""
    DELETING: Container.Status.ValueType  # 3
    """Container is being deleted."""
    ERROR: Container.Status.ValueType  # 4
    """Container failed. The only allowed action is delete."""

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
    FOLDER_ID_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    URL_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    id: builtins.str
    """ID of the container. Generated at creation time."""
    folder_id: builtins.str
    """ID of the folder that the container belongs to."""
    name: builtins.str
    """Name of the container. The name is unique within the folder."""
    description: builtins.str
    """Description of the container."""
    url: builtins.str
    """URL that needs to be requested to call the container."""
    status: global___Container.Status.ValueType
    """Status of the container."""
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Creation timestamp for the container."""

    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Container labels as `key:value` pairs."""

    def __init__(
        self,
        *,
        id: builtins.str = ...,
        folder_id: builtins.str = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        url: builtins.str = ...,
        status: global___Container.Status.ValueType = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["created_at", b"created_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["created_at", b"created_at", "description", b"description", "folder_id", b"folder_id", "id", b"id", "labels", b"labels", "name", b"name", "status", b"status", "url", b"url"]) -> None: ...

global___Container = Container

@typing.final
class Revision(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Status:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _StatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Revision._Status.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        STATUS_UNSPECIFIED: Revision._Status.ValueType  # 0
        CREATING: Revision._Status.ValueType  # 1
        """Revision is being created."""
        ACTIVE: Revision._Status.ValueType  # 2
        """Revision is currently used by the container."""
        OBSOLETE: Revision._Status.ValueType  # 3
        """Revision is not used by the container. May be deleted later."""

    class Status(_Status, metaclass=_StatusEnumTypeWrapper): ...
    STATUS_UNSPECIFIED: Revision.Status.ValueType  # 0
    CREATING: Revision.Status.ValueType  # 1
    """Revision is being created."""
    ACTIVE: Revision.Status.ValueType  # 2
    """Revision is currently used by the container."""
    OBSOLETE: Revision.Status.ValueType  # 3
    """Revision is not used by the container. May be deleted later."""

    ID_FIELD_NUMBER: builtins.int
    CONTAINER_ID_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    IMAGE_FIELD_NUMBER: builtins.int
    RESOURCES_FIELD_NUMBER: builtins.int
    EXECUTION_TIMEOUT_FIELD_NUMBER: builtins.int
    CONCURRENCY_FIELD_NUMBER: builtins.int
    SERVICE_ACCOUNT_ID_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    SECRETS_FIELD_NUMBER: builtins.int
    CONNECTIVITY_FIELD_NUMBER: builtins.int
    PROVISION_POLICY_FIELD_NUMBER: builtins.int
    SCALING_POLICY_FIELD_NUMBER: builtins.int
    LOG_OPTIONS_FIELD_NUMBER: builtins.int
    STORAGE_MOUNTS_FIELD_NUMBER: builtins.int
    id: builtins.str
    """ID of the revision."""
    container_id: builtins.str
    """ID of the container that the revision belongs to."""
    description: builtins.str
    """Description of the revision."""
    concurrency: builtins.int
    """The number of concurrent requests allowed per container instance."""
    service_account_id: builtins.str
    """ID of the service account associated with the revision."""
    status: global___Revision.Status.ValueType
    """Status of the revision."""
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Creation timestamp for the revision."""

    @property
    def image(self) -> global___Image:
        """Image configuration for the revision."""

    @property
    def resources(self) -> global___Resources:
        """Resources allocated to the revision."""

    @property
    def execution_timeout(self) -> google.protobuf.duration_pb2.Duration:
        """Timeout for the execution of the revision.

        If the timeout is exceeded, Serverless Containers responds with a 504 HTTP code.
        """

    @property
    def secrets(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Secret]:
        """Yandex Lockbox secrets to be used by the revision."""

    @property
    def connectivity(self) -> global___Connectivity:
        """Network access. If specified the revision will be attached to specified network/subnet(s)."""

    @property
    def provision_policy(self) -> global___ProvisionPolicy:
        """Policy for provisioning instances of the revision.

        The policy is only applied when the revision is ACTIVE.
        """

    @property
    def scaling_policy(self) -> global___ScalingPolicy:
        """Policy for scaling instances of the revision."""

    @property
    def log_options(self) -> global___LogOptions:
        """Options for logging from the container."""

    @property
    def storage_mounts(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___StorageMount]:
        """S3 mounts to be used by the version."""

    def __init__(
        self,
        *,
        id: builtins.str = ...,
        container_id: builtins.str = ...,
        description: builtins.str = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        image: global___Image | None = ...,
        resources: global___Resources | None = ...,
        execution_timeout: google.protobuf.duration_pb2.Duration | None = ...,
        concurrency: builtins.int = ...,
        service_account_id: builtins.str = ...,
        status: global___Revision.Status.ValueType = ...,
        secrets: collections.abc.Iterable[global___Secret] | None = ...,
        connectivity: global___Connectivity | None = ...,
        provision_policy: global___ProvisionPolicy | None = ...,
        scaling_policy: global___ScalingPolicy | None = ...,
        log_options: global___LogOptions | None = ...,
        storage_mounts: collections.abc.Iterable[global___StorageMount] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["connectivity", b"connectivity", "created_at", b"created_at", "execution_timeout", b"execution_timeout", "image", b"image", "log_options", b"log_options", "provision_policy", b"provision_policy", "resources", b"resources", "scaling_policy", b"scaling_policy"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["concurrency", b"concurrency", "connectivity", b"connectivity", "container_id", b"container_id", "created_at", b"created_at", "description", b"description", "execution_timeout", b"execution_timeout", "id", b"id", "image", b"image", "log_options", b"log_options", "provision_policy", b"provision_policy", "resources", b"resources", "scaling_policy", b"scaling_policy", "secrets", b"secrets", "service_account_id", b"service_account_id", "status", b"status", "storage_mounts", b"storage_mounts"]) -> None: ...

global___Revision = Revision

@typing.final
class Image(google.protobuf.message.Message):
    """Revision image specification."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class EnvironmentEntry(google.protobuf.message.Message):
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

    IMAGE_URL_FIELD_NUMBER: builtins.int
    IMAGE_DIGEST_FIELD_NUMBER: builtins.int
    COMMAND_FIELD_NUMBER: builtins.int
    ARGS_FIELD_NUMBER: builtins.int
    ENVIRONMENT_FIELD_NUMBER: builtins.int
    WORKING_DIR_FIELD_NUMBER: builtins.int
    image_url: builtins.str
    """Image URL, that is used by the revision."""
    image_digest: builtins.str
    """Digest of the image. Calculated at creation time."""
    working_dir: builtins.str
    """Override for the image's WORKDIR."""
    @property
    def command(self) -> global___Command:
        """Override for the image's ENTRYPOINT."""

    @property
    def args(self) -> global___Args:
        """Override for the image's CMD."""

    @property
    def environment(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Additional environment for the container."""

    def __init__(
        self,
        *,
        image_url: builtins.str = ...,
        image_digest: builtins.str = ...,
        command: global___Command | None = ...,
        args: global___Args | None = ...,
        environment: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        working_dir: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["args", b"args", "command", b"command"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["args", b"args", "command", b"command", "environment", b"environment", "image_digest", b"image_digest", "image_url", b"image_url", "working_dir", b"working_dir"]) -> None: ...

global___Image = Image

@typing.final
class Command(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMMAND_FIELD_NUMBER: builtins.int
    @property
    def command(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Command that will override ENTRYPOINT of an image.

        Commands will be executed as is. The runtime will not substitute environment
        variables or execute shell commands. If one wants to do that, they should
        invoke shell interpreter with an appropriate shell script.
        """

    def __init__(
        self,
        *,
        command: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["command", b"command"]) -> None: ...

global___Command = Command

@typing.final
class Args(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ARGS_FIELD_NUMBER: builtins.int
    @property
    def args(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Arguments that will override CMD of an image.

        Arguments will be passed as is. The runtime will not substitute environment
        variables or execute shell commands. If one wants to do that, they should
        invoke shell interpreter with an appropriate shell script.
        """

    def __init__(
        self,
        *,
        args: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["args", b"args"]) -> None: ...

global___Args = Args

@typing.final
class Resources(google.protobuf.message.Message):
    """Resources allocated to a revision."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MEMORY_FIELD_NUMBER: builtins.int
    CORES_FIELD_NUMBER: builtins.int
    CORE_FRACTION_FIELD_NUMBER: builtins.int
    memory: builtins.int
    """Amount of memory available to the revision, specified in bytes, multiple of 128MB."""
    cores: builtins.int
    """Number of cores available to the revision."""
    core_fraction: builtins.int
    """Specifies baseline performance for a core in percent, multiple of 5%.
    Should be 100% for cores > 1.
    """
    def __init__(
        self,
        *,
        memory: builtins.int = ...,
        cores: builtins.int = ...,
        core_fraction: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["core_fraction", b"core_fraction", "cores", b"cores", "memory", b"memory"]) -> None: ...

global___Resources = Resources

@typing.final
class ProvisionPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MIN_INSTANCES_FIELD_NUMBER: builtins.int
    min_instances: builtins.int
    """Minimum number of guaranteed provisioned container instances for all zones
    in total.
    """
    def __init__(
        self,
        *,
        min_instances: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["min_instances", b"min_instances"]) -> None: ...

global___ProvisionPolicy = ProvisionPolicy

@typing.final
class Secret(google.protobuf.message.Message):
    """Secret that is available to the container at run time."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    VERSION_ID_FIELD_NUMBER: builtins.int
    KEY_FIELD_NUMBER: builtins.int
    ENVIRONMENT_VARIABLE_FIELD_NUMBER: builtins.int
    id: builtins.str
    """ID of Yandex Lockbox secret."""
    version_id: builtins.str
    """ID of Yandex Lockbox secret."""
    key: builtins.str
    """Key in secret's payload, which value to be delivered into container environment."""
    environment_variable: builtins.str
    """Environment variable in which secret's value is delivered."""
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        version_id: builtins.str = ...,
        key: builtins.str = ...,
        environment_variable: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["environment_variable", b"environment_variable", "reference", b"reference"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["environment_variable", b"environment_variable", "id", b"id", "key", b"key", "reference", b"reference", "version_id", b"version_id"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["reference", b"reference"]) -> typing.Literal["environment_variable"] | None: ...

global___Secret = Secret

@typing.final
class Connectivity(google.protobuf.message.Message):
    """Revision connectivity specification."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NETWORK_ID_FIELD_NUMBER: builtins.int
    SUBNET_IDS_FIELD_NUMBER: builtins.int
    network_id: builtins.str
    """Network the revision will have access to."""
    @property
    def subnet_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """The list of subnets (from the same network) the revision can be attached to.

        Deprecated, it is sufficient to specify only network_id, without the list of subnet_ids.
        """

    def __init__(
        self,
        *,
        network_id: builtins.str = ...,
        subnet_ids: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["network_id", b"network_id", "subnet_ids", b"subnet_ids"]) -> None: ...

global___Connectivity = Connectivity

@typing.final
class LogOptions(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DISABLED_FIELD_NUMBER: builtins.int
    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    FOLDER_ID_FIELD_NUMBER: builtins.int
    MIN_LEVEL_FIELD_NUMBER: builtins.int
    disabled: builtins.bool
    """Is logging from container disabled."""
    log_group_id: builtins.str
    """Entry should be written to log group resolved by ID."""
    folder_id: builtins.str
    """Entry should be written to default log group for specified folder."""
    min_level: yandex.cloud.logging.v1.log_entry_pb2.LogLevel.Level.ValueType
    """Minimum log entry level.

    See [LogLevel.Level] for details.
    """
    def __init__(
        self,
        *,
        disabled: builtins.bool = ...,
        log_group_id: builtins.str = ...,
        folder_id: builtins.str = ...,
        min_level: yandex.cloud.logging.v1.log_entry_pb2.LogLevel.Level.ValueType = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["destination", b"destination", "folder_id", b"folder_id", "log_group_id", b"log_group_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["destination", b"destination", "disabled", b"disabled", "folder_id", b"folder_id", "log_group_id", b"log_group_id", "min_level", b"min_level"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["destination", b"destination"]) -> typing.Literal["log_group_id", "folder_id"] | None: ...

global___LogOptions = LogOptions

@typing.final
class ScalingPolicy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ZONE_INSTANCES_LIMIT_FIELD_NUMBER: builtins.int
    ZONE_REQUESTS_LIMIT_FIELD_NUMBER: builtins.int
    zone_instances_limit: builtins.int
    """Upper limit for instance count in each zone.
    0 means no limit.
    """
    zone_requests_limit: builtins.int
    """Upper limit of requests count in each zone.
    0 means no limit.
    """
    def __init__(
        self,
        *,
        zone_instances_limit: builtins.int = ...,
        zone_requests_limit: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["zone_instances_limit", b"zone_instances_limit", "zone_requests_limit", b"zone_requests_limit"]) -> None: ...

global___ScalingPolicy = ScalingPolicy

@typing.final
class StorageMount(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BUCKET_ID_FIELD_NUMBER: builtins.int
    PREFIX_FIELD_NUMBER: builtins.int
    READ_ONLY_FIELD_NUMBER: builtins.int
    MOUNT_POINT_PATH_FIELD_NUMBER: builtins.int
    bucket_id: builtins.str
    """S3 bucket name for mounting."""
    prefix: builtins.str
    """S3 bucket prefix for mounting."""
    read_only: builtins.bool
    """Is mount read only."""
    mount_point_path: builtins.str
    """Mount point path inside the container for mounting."""
    def __init__(
        self,
        *,
        bucket_id: builtins.str = ...,
        prefix: builtins.str = ...,
        read_only: builtins.bool = ...,
        mount_point_path: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["bucket_id", b"bucket_id", "mount_point_path", b"mount_point_path", "prefix", b"prefix", "read_only", b"read_only"]) -> None: ...

global___StorageMount = StorageMount
