"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.struct_pb2
import google.protobuf.timestamp_pb2
import sys
import typing
import yandex.cloud.logging.v1.log_resource_pb2

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class LogEntry(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UID_FIELD_NUMBER: builtins.int
    RESOURCE_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    INGESTED_AT_FIELD_NUMBER: builtins.int
    SAVED_AT_FIELD_NUMBER: builtins.int
    LEVEL_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    JSON_PAYLOAD_FIELD_NUMBER: builtins.int
    STREAM_NAME_FIELD_NUMBER: builtins.int
    uid: builtins.str
    """Unique entry ID.

    Useful for logs deduplication.
    """
    level: global___LogLevel.Level.ValueType
    """Entry severity.

    See [LogLevel.Level] for details.
    """
    message: builtins.str
    """Entry text message."""
    stream_name: builtins.str
    """Entry stream name."""
    @property
    def resource(self) -> yandex.cloud.logging.v1.log_resource_pb2.LogEntryResource:
        """Entry resource specification.

        May contain information about source service and resource ID.
        Also may be provided by the user.
        """

    @property
    def timestamp(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Timestamp of the entry."""

    @property
    def ingested_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Entry ingestion time observed by [LogIngestionService]."""

    @property
    def saved_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Entry save time.

        Entry is ready to be read since this moment.
        """

    @property
    def json_payload(self) -> google.protobuf.struct_pb2.Struct:
        """Entry annotation."""

    def __init__(
        self,
        *,
        uid: builtins.str = ...,
        resource: yandex.cloud.logging.v1.log_resource_pb2.LogEntryResource | None = ...,
        timestamp: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        ingested_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        saved_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        level: global___LogLevel.Level.ValueType = ...,
        message: builtins.str = ...,
        json_payload: google.protobuf.struct_pb2.Struct | None = ...,
        stream_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["ingested_at", b"ingested_at", "json_payload", b"json_payload", "resource", b"resource", "saved_at", b"saved_at", "timestamp", b"timestamp"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["ingested_at", b"ingested_at", "json_payload", b"json_payload", "level", b"level", "message", b"message", "resource", b"resource", "saved_at", b"saved_at", "stream_name", b"stream_name", "timestamp", b"timestamp", "uid", b"uid"]) -> None: ...

global___LogEntry = LogEntry

@typing.final
class IncomingLogEntry(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TIMESTAMP_FIELD_NUMBER: builtins.int
    LEVEL_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    JSON_PAYLOAD_FIELD_NUMBER: builtins.int
    STREAM_NAME_FIELD_NUMBER: builtins.int
    level: global___LogLevel.Level.ValueType
    """Entry severity.

    See [LogLevel.Level] for details.
    """
    message: builtins.str
    """Entry text message."""
    stream_name: builtins.str
    """Entry stream name."""
    @property
    def timestamp(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Timestamp of the entry."""

    @property
    def json_payload(self) -> google.protobuf.struct_pb2.Struct:
        """Entry annotation."""

    def __init__(
        self,
        *,
        timestamp: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        level: global___LogLevel.Level.ValueType = ...,
        message: builtins.str = ...,
        json_payload: google.protobuf.struct_pb2.Struct | None = ...,
        stream_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["json_payload", b"json_payload", "timestamp", b"timestamp"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["json_payload", b"json_payload", "level", b"level", "message", b"message", "stream_name", b"stream_name", "timestamp", b"timestamp"]) -> None: ...

global___IncomingLogEntry = IncomingLogEntry

@typing.final
class LogEntryDefaults(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LEVEL_FIELD_NUMBER: builtins.int
    JSON_PAYLOAD_FIELD_NUMBER: builtins.int
    STREAM_NAME_FIELD_NUMBER: builtins.int
    level: global___LogLevel.Level.ValueType
    """Default entry severity.
    Will be applied if entry level is unspecified.

    See [LogLevel.Level] for details.
    """
    stream_name: builtins.str
    """Entry stream name."""
    @property
    def json_payload(self) -> google.protobuf.struct_pb2.Struct:
        """Default entry annotation.
        Will be merged with entry annotation.
        Any conflict will be resolved in favor of entry own annotation.
        """

    def __init__(
        self,
        *,
        level: global___LogLevel.Level.ValueType = ...,
        json_payload: google.protobuf.struct_pb2.Struct | None = ...,
        stream_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["json_payload", b"json_payload"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["json_payload", b"json_payload", "level", b"level", "stream_name", b"stream_name"]) -> None: ...

global___LogEntryDefaults = LogEntryDefaults

@typing.final
class Destination(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    FOLDER_ID_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """Entry should be written to log group resolved by ID."""
    folder_id: builtins.str
    """Entry should be written to default log group for the folder."""
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
        folder_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["destination", b"destination", "folder_id", b"folder_id", "log_group_id", b"log_group_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["destination", b"destination", "folder_id", b"folder_id", "log_group_id", b"log_group_id"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["destination", b"destination"]) -> typing.Literal["log_group_id", "folder_id"] | None: ...

global___Destination = Destination

@typing.final
class LogLevel(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Level:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _LevelEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[LogLevel._Level.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        LEVEL_UNSPECIFIED: LogLevel._Level.ValueType  # 0
        """Default log level.

        Equivalent to not specifying log level at all.
        """
        TRACE: LogLevel._Level.ValueType  # 1
        """Trace log level.

        Possible use case: verbose logging of some business logic.
        """
        DEBUG: LogLevel._Level.ValueType  # 2
        """Debug log level.

        Possible use case: debugging special cases in application logic.
        """
        INFO: LogLevel._Level.ValueType  # 3
        """Info log level.

        Mostly used for information messages.
        """
        WARN: LogLevel._Level.ValueType  # 4
        """Warn log level.

        May be used to alert about significant events.
        """
        ERROR: LogLevel._Level.ValueType  # 5
        """Error log level.

        May be used to alert about errors in infrastructure, logic, etc.
        """
        FATAL: LogLevel._Level.ValueType  # 6
        """Fatal log level.

        May be used to alert about unrecoverable failures and events.
        """

    class Level(_Level, metaclass=_LevelEnumTypeWrapper):
        """Possible log levels for entries."""

    LEVEL_UNSPECIFIED: LogLevel.Level.ValueType  # 0
    """Default log level.

    Equivalent to not specifying log level at all.
    """
    TRACE: LogLevel.Level.ValueType  # 1
    """Trace log level.

    Possible use case: verbose logging of some business logic.
    """
    DEBUG: LogLevel.Level.ValueType  # 2
    """Debug log level.

    Possible use case: debugging special cases in application logic.
    """
    INFO: LogLevel.Level.ValueType  # 3
    """Info log level.

    Mostly used for information messages.
    """
    WARN: LogLevel.Level.ValueType  # 4
    """Warn log level.

    May be used to alert about significant events.
    """
    ERROR: LogLevel.Level.ValueType  # 5
    """Error log level.

    May be used to alert about errors in infrastructure, logic, etc.
    """
    FATAL: LogLevel.Level.ValueType  # 6
    """Fatal log level.

    May be used to alert about unrecoverable failures and events.
    """

    LEVEL_FIELD_NUMBER: builtins.int
    level: global___LogLevel.Level.ValueType
    """Entry level.

    See [Level] for possible values.
    """
    def __init__(
        self,
        *,
        level: global___LogLevel.Level.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["level", b"level"]) -> None: ...

global___LogLevel = LogLevel
