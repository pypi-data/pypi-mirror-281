"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.wrappers_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class RedisConfig7_0(google.protobuf.message.Message):
    """Fields and structure of `RedisConfig` reflects Redis configuration file
    parameters.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _MaxmemoryPolicy:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _MaxmemoryPolicyEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[RedisConfig7_0._MaxmemoryPolicy.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        MAXMEMORY_POLICY_UNSPECIFIED: RedisConfig7_0._MaxmemoryPolicy.ValueType  # 0
        VOLATILE_LRU: RedisConfig7_0._MaxmemoryPolicy.ValueType  # 1
        """Try to remove less recently used (LRU) keys with `expire set`."""
        ALLKEYS_LRU: RedisConfig7_0._MaxmemoryPolicy.ValueType  # 2
        """Remove less recently used (LRU) keys."""
        VOLATILE_LFU: RedisConfig7_0._MaxmemoryPolicy.ValueType  # 3
        """Try to remove least frequently used (LFU) keys with `expire set`."""
        ALLKEYS_LFU: RedisConfig7_0._MaxmemoryPolicy.ValueType  # 4
        """Remove least frequently used (LFU) keys."""
        VOLATILE_RANDOM: RedisConfig7_0._MaxmemoryPolicy.ValueType  # 5
        """Try to remove keys with `expire set` randomly."""
        ALLKEYS_RANDOM: RedisConfig7_0._MaxmemoryPolicy.ValueType  # 6
        """Remove keys randomly."""
        VOLATILE_TTL: RedisConfig7_0._MaxmemoryPolicy.ValueType  # 7
        """Try to remove less recently used (LRU) keys with `expire set`
        and shorter TTL first.
        """
        NOEVICTION: RedisConfig7_0._MaxmemoryPolicy.ValueType  # 8
        """Return errors when memory limit was reached and commands could require
        more memory to be used.
        """

    class MaxmemoryPolicy(_MaxmemoryPolicy, metaclass=_MaxmemoryPolicyEnumTypeWrapper): ...
    MAXMEMORY_POLICY_UNSPECIFIED: RedisConfig7_0.MaxmemoryPolicy.ValueType  # 0
    VOLATILE_LRU: RedisConfig7_0.MaxmemoryPolicy.ValueType  # 1
    """Try to remove less recently used (LRU) keys with `expire set`."""
    ALLKEYS_LRU: RedisConfig7_0.MaxmemoryPolicy.ValueType  # 2
    """Remove less recently used (LRU) keys."""
    VOLATILE_LFU: RedisConfig7_0.MaxmemoryPolicy.ValueType  # 3
    """Try to remove least frequently used (LFU) keys with `expire set`."""
    ALLKEYS_LFU: RedisConfig7_0.MaxmemoryPolicy.ValueType  # 4
    """Remove least frequently used (LFU) keys."""
    VOLATILE_RANDOM: RedisConfig7_0.MaxmemoryPolicy.ValueType  # 5
    """Try to remove keys with `expire set` randomly."""
    ALLKEYS_RANDOM: RedisConfig7_0.MaxmemoryPolicy.ValueType  # 6
    """Remove keys randomly."""
    VOLATILE_TTL: RedisConfig7_0.MaxmemoryPolicy.ValueType  # 7
    """Try to remove less recently used (LRU) keys with `expire set`
    and shorter TTL first.
    """
    NOEVICTION: RedisConfig7_0.MaxmemoryPolicy.ValueType  # 8
    """Return errors when memory limit was reached and commands could require
    more memory to be used.
    """

    @typing.final
    class ClientOutputBufferLimit(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        HARD_LIMIT_FIELD_NUMBER: builtins.int
        SOFT_LIMIT_FIELD_NUMBER: builtins.int
        SOFT_SECONDS_FIELD_NUMBER: builtins.int
        @property
        def hard_limit(self) -> google.protobuf.wrappers_pb2.Int64Value:
            """Total limit in bytes."""

        @property
        def soft_limit(self) -> google.protobuf.wrappers_pb2.Int64Value:
            """Limit in bytes during certain time period."""

        @property
        def soft_seconds(self) -> google.protobuf.wrappers_pb2.Int64Value:
            """Seconds for soft limit."""

        def __init__(
            self,
            *,
            hard_limit: google.protobuf.wrappers_pb2.Int64Value | None = ...,
            soft_limit: google.protobuf.wrappers_pb2.Int64Value | None = ...,
            soft_seconds: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["hard_limit", b"hard_limit", "soft_limit", b"soft_limit", "soft_seconds", b"soft_seconds"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["hard_limit", b"hard_limit", "soft_limit", b"soft_limit", "soft_seconds", b"soft_seconds"]) -> None: ...

    MAXMEMORY_POLICY_FIELD_NUMBER: builtins.int
    TIMEOUT_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    DATABASES_FIELD_NUMBER: builtins.int
    SLOWLOG_LOG_SLOWER_THAN_FIELD_NUMBER: builtins.int
    SLOWLOG_MAX_LEN_FIELD_NUMBER: builtins.int
    NOTIFY_KEYSPACE_EVENTS_FIELD_NUMBER: builtins.int
    CLIENT_OUTPUT_BUFFER_LIMIT_PUBSUB_FIELD_NUMBER: builtins.int
    CLIENT_OUTPUT_BUFFER_LIMIT_NORMAL_FIELD_NUMBER: builtins.int
    MAXMEMORY_PERCENT_FIELD_NUMBER: builtins.int
    maxmemory_policy: global___RedisConfig7_0.MaxmemoryPolicy.ValueType
    """Redis key eviction policy for a dataset that reaches maximum memory,
    available to the host. Redis maxmemory setting depends on Managed
    Service for Redis [host class](/docs/managed-redis/concepts/instance-types).

    All policies are described in detail in [Redis documentation](https://redis.io/topics/lru-cache).
    """
    password: builtins.str
    """Authentication password."""
    notify_keyspace_events: builtins.str
    """String setting for pub\\sub functionality."""
    @property
    def timeout(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Time that Redis keeps the connection open while the client is idle.
        If no new command is sent during that time, the connection is closed.
        """

    @property
    def databases(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Number of database buckets on a single redis-server process."""

    @property
    def slowlog_log_slower_than(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Threshold for logging slow requests to server in microseconds (log only slower than it)."""

    @property
    def slowlog_max_len(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Max slow requests number to log."""

    @property
    def client_output_buffer_limit_pubsub(self) -> global___RedisConfig7_0.ClientOutputBufferLimit:
        """Redis connection output buffers limits for pubsub operations."""

    @property
    def client_output_buffer_limit_normal(self) -> global___RedisConfig7_0.ClientOutputBufferLimit:
        """Redis connection output buffers limits for clients."""

    @property
    def maxmemory_percent(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Redis maxmemory percent"""

    def __init__(
        self,
        *,
        maxmemory_policy: global___RedisConfig7_0.MaxmemoryPolicy.ValueType = ...,
        timeout: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        password: builtins.str = ...,
        databases: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        slowlog_log_slower_than: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        slowlog_max_len: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        notify_keyspace_events: builtins.str = ...,
        client_output_buffer_limit_pubsub: global___RedisConfig7_0.ClientOutputBufferLimit | None = ...,
        client_output_buffer_limit_normal: global___RedisConfig7_0.ClientOutputBufferLimit | None = ...,
        maxmemory_percent: google.protobuf.wrappers_pb2.Int64Value | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["client_output_buffer_limit_normal", b"client_output_buffer_limit_normal", "client_output_buffer_limit_pubsub", b"client_output_buffer_limit_pubsub", "databases", b"databases", "maxmemory_percent", b"maxmemory_percent", "slowlog_log_slower_than", b"slowlog_log_slower_than", "slowlog_max_len", b"slowlog_max_len", "timeout", b"timeout"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["client_output_buffer_limit_normal", b"client_output_buffer_limit_normal", "client_output_buffer_limit_pubsub", b"client_output_buffer_limit_pubsub", "databases", b"databases", "maxmemory_percent", b"maxmemory_percent", "maxmemory_policy", b"maxmemory_policy", "notify_keyspace_events", b"notify_keyspace_events", "password", b"password", "slowlog_log_slower_than", b"slowlog_log_slower_than", "slowlog_max_len", b"slowlog_max_len", "timeout", b"timeout"]) -> None: ...

global___RedisConfig7_0 = RedisConfig7_0

@typing.final
class RedisConfigSet7_0(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EFFECTIVE_CONFIG_FIELD_NUMBER: builtins.int
    USER_CONFIG_FIELD_NUMBER: builtins.int
    DEFAULT_CONFIG_FIELD_NUMBER: builtins.int
    @property
    def effective_config(self) -> global___RedisConfig7_0:
        """Effective settings for a Redis 7.0 cluster (a combination of settings
        defined in [user_config] and [default_config]).
        """

    @property
    def user_config(self) -> global___RedisConfig7_0:
        """User-defined settings for a Redis 7.0 cluster."""

    @property
    def default_config(self) -> global___RedisConfig7_0:
        """Default configuration for a Redis 7.0 cluster."""

    def __init__(
        self,
        *,
        effective_config: global___RedisConfig7_0 | None = ...,
        user_config: global___RedisConfig7_0 | None = ...,
        default_config: global___RedisConfig7_0 | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["default_config", b"default_config", "effective_config", b"effective_config", "user_config", b"user_config"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["default_config", b"default_config", "effective_config", b"effective_config", "user_config", b"user_config"]) -> None: ...

global___RedisConfigSet7_0 = RedisConfigSet7_0
